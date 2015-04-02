from time import sleep
from abc import abstractmethod
import json
import logging

import threading
from datetime import datetime, timedelta

import pyzenobase
from .settings import Settings, SettingsException

from typing import Iterable, List, Set


class Activity(dict):
    """
    Used to represents an activity or event.
    """
    def __init__(self, tags: List[str], started_at: datetime, ended_at: datetime, **kwargs):
        dict.__init__(self)
        self["tags"] = tags
        if "cmd" in kwargs:
            # TODO: Keep?
            cmd = kwargs.pop("cmd")
            cmd = list(filter(lambda s: s[0] != "-", cmd))
            self["cmd"] = cmd
        self["start"] = started_at
        self["end"] = ended_at

        self.update(kwargs)

        msg = ""
        msg += "Logged activity '{}':".format(tags)
        msg += "  Started: {}".format(self["start"])
        msg += "  Ended: {}".format(self["end"])
        msg += "  Duration: {}".format(self.duration)
        if "cmd" in self:
            msg += "  Command: {}".format(self["cmd"])
        logging.debug(msg)

    @property
    def start(self) -> datetime:
        return self["start"]

    @start.setter
    def start(self, start: datetime):
        self["start"] = start

    @property
    def end(self) -> datetime:
        return self["end"]

    @end.setter
    def end(self, end: datetime):
        self["end"] = end

    @property
    def tags(self) -> List[str]:
        return self["tags"]

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def to_zenobase_event(self) -> pyzenobase.ZenobaseEvent:
        # TODO: Add misc fields into note field
        data = {"tag": self.tags,
                "timestamp": self.start,
                "duration": self.duration.total_seconds()*1000}
        return pyzenobase.ZenobaseEvent(data)

    def to_json_dict(self) -> dict:
        data = self.copy()
        data["start"] = data["start"].isoformat()
        data["end"] = data["end"].isoformat()
        return data

    def to_json_str(self) -> str:
        data = self.to_json_dict()
        return json.dumps(data)


class Agent(threading.Thread):
    """Base class for Watchers, Filters and Watchers"""

    def __init__(self):
        # TODO: This will run twice for Filters which will run both Watcher.__init__ and Logger.__init__
        threading.Thread.__init__(self, name=self.__class__.__name__)

    @abstractmethod
    def run(self):
        pass

    @property
    def identifier(self):
        """Identifier for agent, used in settings and as a module name shorter than the class name"""
        return self.name[0:-len(self.agent_type)].lower()

    @property
    def settings(self):
        """Returns the settings for the current module from the global settings"""
        if not self.identifier:
            raise Exception("identifier was not set, could not get settings")
        settings = Settings()
        if self.agent_type+"s" not in settings:
            raise SettingsException("settings file appears to be corrupt, root-level key {} not found"
                                    .format(self.agent_type + "s"))
        if self.identifier in settings[self.agent_type+"s"]:
            return settings[self.agent_type+"s"][self.identifier]
        else:
            settings[self.agent_type][self.identifier] = self.default_settings
            logging.warning("Settings for agent '{}' missing, creating entry with defaults")

    @property
    def agent_type(self) -> str:
        """
        Returns the agent_type of the Agent,
        can be "filter", "logger" or "watcher.
        """
        if isinstance(self, Filter):
            return "filter"
        elif isinstance(self, Logger):
            return "logger"
        elif isinstance(self, Watcher):
            return "watcher"
        else:
            raise Exception("Unknown agent type")

    @property
    def default_settings(self):
        """Default settings for agent, will be inserted into settingsfile if entry is missing. Override to change."""
        return {}


class Logger(Agent):
    """
    Base class for loggers

    Listens to watchers and/or filters and logs activities with a
    method that should be defined by the subclass.
    """

    def __init__(self):
        Agent.__init__(self)
        self.watchers = set()  # type: Set[Watcher]

        # Must be thread-safe
        self._activities = []
        self._activities_lock = threading.Lock()
        self._activities_in_queue_event = threading.Event()

    # Only here to keep editor from complaining about unimplemented method
    def run(self):
        while True:
            self.wait()
            activities = self.flush_activities()
            if len(activities) > 0:
                try:
                    self.log(activities)
                    logging.info("{} logged {} activities".format(self.name, len(activities)))
                except Exception:
                    logging.error("An error occurred while trying to log activities, " +
                                  "readding {} activities to log-queue.".format(len(activities)), exc_info=True)
                    self.add_activities(activities)

    @abstractmethod
    def wait(self):
        """
        Usually runs `sleep(10)` or `self.wait_for_activities()`
        """

    @abstractmethod
    def log(self, activities: List[Activity]):
        """
        Do whatever you wish to activities
        """

    # TODO: Use Optional[int] type annotation when the new mypy is on PyPI
    def wait_for_activities(self, timeout: int=None):
        """
        Blocks until there are activities in the queue
        to be retrieved with flush_activities
        """
        self._activities_in_queue_event.wait(timeout)

    @property
    def has_activities_in_queue(self) -> bool:
        return self._activities_in_queue_event.is_set()

    def add_activity(self, activity: Activity):
        """
        Adds a single activity to the queue
        """
        if not isinstance(activity, Activity):
            raise TypeError("{} is not an Activity".format(activity))
        with self._activities_lock:
            self._activities.append(activity)
            self._activities_in_queue_event.set()

    def add_activities(self, activities: Iterable[Activity]):
        """
        Adds an iterable of activities to the queue
        """
        for activity in activities:
            self.add_activity(activity)

    def flush_activities(self) -> List[Activity]:
        """
        Retrieves, removes and then returns all activities from the queue
        """
        with self._activities_lock:
            activities = self._activities
            self._activities = []
            self._activities_in_queue_event.clear()
        return activities

    def add_watcher(self, watcher: 'Watcher'):
        """
        Adds a watcher to the logger, if the logger isn't
        registered with the watcher it sets that up as well.
        """
        if not isinstance(watcher, Watcher):
            raise TypeError("{} is not a Watcher".format(watcher))

        self.watchers.add(watcher)
        if self not in watcher.loggers:
            watcher.add_logger(self)

    def add_watchers(self, watchers: 'Iterable[Watcher]'):
        """
        Does the same as add_watcher, but for an iterable of watchers.
        """
        for watcher in watchers:
            self.add_watcher(watcher)


class Watcher(Agent):
    """
    Base class for watchers

    Watches for activities with a method that should be defined by the
    subclass and forwards those activities to connected loggers and/or
    filters.
    """

    def __init__(self):
        Agent.__init__(self)
        self.loggers = set()  # type: Set[Logger]

    # Only here to keep editor from complaining about unimplemented method
    @abstractmethod
    def run(self):
        pass

    def add_logger(self, logger: Logger):
        """
        Adds a single logger to the watcher, if the watcher isn't
        registered with the logger it sets that up as well.
        """
        if not isinstance(logger, Logger):
            raise TypeError("{} was not a Logger".format(logger))

        self.loggers.add(logger)
        if self not in logger.watchers:
            logger.add_watcher(self)

    def add_loggers(self, loggers: Iterable[Logger]):
        for logger in loggers:
            self.add_logger(logger)

    def dispatch_activity(self, activity: Activity):
        """
        Sends a single activity to the queues of all listening loggers.
        """
        for logger in self.loggers:
            logger.add_activity(activity)

    def dispatch_activities(self, activities: Iterable[Activity]):
        """
        Sends a iterable of activities to the queues of all listening loggers.
        """
        for logger in self.loggers:
            logger.add_activities(activities)


class Filter(Logger, Watcher):
    """
    Base class for filters

    Acts as both a logger and a watcher, effectively being able to do
    certain operations on the received activities before sending them
    forward in the chain.
    """

    def __init__(self):
        Logger.__init__(self)
        Watcher.__init__(self)

    @abstractmethod
    def process(self, activities: List[Activity]) -> List[Activity]:
        """
        Does a set of operations on the activities
        """
        pass

    @abstractmethod
    def wait(self):
        pass

    def log(self, activities: List[Activity]):
        self.dispatch_activities(activities)

    def run(self):
        while True:
            self.wait()
            activities = self.flush_activities()
            if len(activities) == 0:
                continue

            try:
                activities = self.process(activities)
            except Exception as e:
                logging.error("Error while trying to process activities")
                break

            self.log(activities)
            logging.info("{} dispatched {} activities".format(self.name, len(activities)))