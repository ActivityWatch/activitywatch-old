#!/usr/bin/python3

import os
import sys
import subprocess
import unittest
import logging
import threading

import time
from time import sleep

from datetime import datetime


class Activity(dict):                                                                    
    def __init__(self, window_class, started_at, ended_at, cmd=None):                    
        dict.__init__(self)                                                              
        self["window_class"] = window_class                                              
        if cmd:                                                                          
            cmd = list(filter(lambda s: s[0] != "-", cmd))                               
            self["cmd"] = cmd                                                            
        self["start"] = started_at                                                       
        self["end"] = ended_at                                                           
        self["duration"] = ended_at - started_at                                         
                                                                                         
        print("\nLogged activity '{}':".format(window_class))                            
        print("  Command: {}\n  Window selected for: {}\n".format(cmd, self["duration"]))
                                                                                         
    def to_zenobase_event(self):                                                         
        # TODO                                                                           
        pass                                                                             


class Logger(threading.Thread):
    """Listens to watchers and logs activities"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.watchers = []

        # Must be thread-safe
        self._activities = []
        self._activities_lock = threading.Lock()

    def run(self):
        raise NotImplementedError("run method must be implemented in Logger subclass")

    def add_activity(self, activity):
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


class Watcher(threading.Thread):
    """Base class for a watcher"""

    def __init__(self):
        threading.Thread.__init__(self)
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
