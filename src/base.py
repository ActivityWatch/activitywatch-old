import json
import logging

import threading
from datetime import datetime

import pyzenobase
from settings import Settings, SettingsException


class Activity(dict):                                                                    
    def __init__(self, tags: "string or string[]", started_at, ended_at, **kwargs):
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

    def duration(self):
        return self["end"] - self["start"]

    def to_zenobase_event(self):
        # TODO: Add misc fields into note field
        data = {"tag": self["tags"],
                "timestamp": self["start"],
                "duration": self.duration().total_seconds()*1000}
        return pyzenobase.ZenobaseEvent(data)

    def to_json_dict(self):
        data = self.copy()
        data["start"] = data["start"].isoformat()
        data["end"] = data["end"].isoformat()
        return data

    def to_json(self):
        data = self.to_json_dict()
        return json.dumps(data)


class Agent(threading.Thread):
    """Base class for Watchers, Filters and Watchers"""
    def __init__(self, type, name):
        threading.Thread.__init__(self, name=self.__class__.__name__)

        self.logger = logging.Logger(self.__class__.__name__)

        settings = Settings()
        if type+"s" in settings and name in settings[type+"s"]:
            self.settings = settings[type+"s"][name]
        else:
            raise SettingsException("missing entry in settings file")


class Logger(Agent):
    """Listens to watchers and logs activities"""

    def __init__(self, name):
        Agent.__init__(self, "logger", name)
        self.watchers = []

        # Must be thread-safe
        self._activities = []
        self._activities_lock = threading.Lock()

    def run(self):
        raise NotImplementedError("run method must be implemented in Logger subclass")

    def add_activity(self, activity):
        if not isinstance(activity, Activity):
            raise TypeError("{} is not an Activity".format(activity))
        with self._activities_lock:
            self._activities.append(activity)

    def flush_activities(self):
        with self._activities_lock:
            activities = self._activities
            self._activities = []
        return activities

    def add_watcher(self, watcher):
        """Start listening to watchers here"""
        if not isinstance(watcher, Watcher):
            raise TypeError("{} is not a Watcher".format(watcher))
        watcher._add_logger(self)
        self.watchers.append(watcher)


class Watcher(Agent):
    """Base class for a watcher"""

    def __init__(self, name):
        Agent.__init__(self, "watcher", name)
        self.loggers = []

    def _add_logger(self, logger):
        """Should only be called from Logger.add_watcher"""
        if not isinstance(logger, Logger):
            raise TypeError("{} was not a Logger".format(logger))
        self.loggers.append(logger)

    def run(self):
        raise NotImplementedError("Watchers must implement the run method")

    def add_activity(self, activity):
        for logger in self.loggers:
            logger.add_activity(activity)
