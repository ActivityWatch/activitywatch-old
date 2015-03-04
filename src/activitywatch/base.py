import json
import logging

import threading
from datetime import datetime, timedelta

import pyzenobase
from .settings import Settings, SettingsException


class Activity(dict):                                                                    
    def __init__(self, tags: str or "list[str]", started_at, ended_at, **kwargs):
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
        msg += "  Duration: {}".format(self.duration())
        if "cmd" in self:
            msg += "  Command: {}".format(self["cmd"])
        logging.debug(msg)

    def duration(self) -> timedelta:
        return self["end"] - self["start"]

    def to_zenobase_event(self) -> pyzenobase.ZenobaseEvent:
        # TODO: Add misc fields into note field
        data = {"tag": self["tags"],
                "timestamp": self["start"],
                "duration": self.duration().total_seconds()*1000}
        return pyzenobase.ZenobaseEvent(data)

    def to_json_dict(self) -> dict:
        data = self.copy()
        data["start"] = data["start"].isoformat()
        data["end"] = data["end"].isoformat()
        return data

    def to_json(self) -> str:
        data = self.to_json_dict()
        return json.dumps(data)


class Agent(threading.Thread):
    """Base class for Watchers, Filters and Watchers"""
    NAME = ""

    def __init__(self):
        threading.Thread.__init__(self, name=self.__class__.__name__)

        if not self.NAME:
            raise Exception("NAME can not be empty")

        agent_type = self.get_agent_type()
        settings = Settings()
        if agent_type+"s" in settings and self.NAME in settings[agent_type+"s"]:
            self.settings = settings[agent_type+"s"][self.NAME]
        else:
            raise SettingsException("missing entry in settings file")

    def get_agent_type(self) -> str:
        if isinstance(self, Logger) and isinstance(self, Watcher):
            return "filter"
        elif isinstance(self, Logger):
            return "logger"
        elif isinstance(self, Watcher):
            return "watcher"
        else:
            raise Exception("Unknown agent type")


class Logger(Agent):
    """Listens to watchers and logs activities"""

    def __init__(self):
        Agent.__init__(self)
        self.watchers = set()

        # Must be thread-safe
        self._activities = []
        self._activities_lock = threading.Lock()

    def run(self):
        raise NotImplementedError("run method must be implemented in Logger subclass")

    def add_activity(self, activity: Activity):
        if not isinstance(activity, Activity):
            raise TypeError("{} is not an Activity".format(activity))
        with self._activities_lock:
            self._activities.append(activity)

    def flush_activities(self) -> "list[Activity]":
        with self._activities_lock:
            activities = self._activities
            self._activities = []
        return activities

    def add_watcher(self, watcher: "Watcher"):
        """Start listening to watchers here"""
        if not isinstance(watcher, Watcher):
            raise TypeError("{} is not a Watcher".format(watcher))
        watcher._add_logger(self)
        self.watchers.add(watcher)


class Watcher(Agent):
    """Base class for a watcher"""

    def __init__(self):
        Agent.__init__(self)
        self.loggers = set()

    def _add_logger(self, logger: Logger):
        """Should only be called from Logger.add_watcher"""
        if not isinstance(logger, Logger):
            raise TypeError("{} was not a Logger".format(logger))
        self.loggers.add(logger)

    def run(self):
        raise NotImplementedError("Watchers must implement the run method")

    def add_activity(self, activity: Activity):
        for logger in self.loggers:
            logger.add_activity(activity)
