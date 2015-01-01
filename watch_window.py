#!/usr/bin/python3

#####################
#  Stdlib Packages  #
#####################

import os
import sys
import subprocess
import unittest
import logging
import threading

import time
from time import sleep

from datetime import datetime

#####################
# External packages #
#####################

import psutil

import Xlib
import Xlib.display
from Xlib import X, Xatom

import pyzenobase


WATCH_INTERVAL = 1.0


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


class X11Watcher(Watcher):
    """Watches activity in X11"""
    # TODO: Move window helper functions to container class for xlib's Window

    def __init__(self):
        Watcher.__init__(self)
        self.display = Xlib.display.Display()
        self.screen = self.display.screen()

        self._last_window = None
        self._active_window = None

    @property
    def last_window(self):
        return self._last_window

    def update_last_window(self):
        self.last_selected_at = datetime.now()
        self._last_window = self.active_window

    @property
    def active_window(self):
        return self._active_window

    def update_active_window(self):
        atom = self.display.get_atom("_NET_ACTIVE_WINDOW")
        w = self.screen.root.get_full_property(atom, X.AnyPropertyType)
        w_id = w.value[-1]
        self._active_window = self.get_window(w_id)

    def run(self):
        self.update_active_window()
        window = self.active_window
        
        name, cls = self.get_window_name(window)
        pid = self.get_window_pid(window)
        print("First focus is '{}' with PID: {}".format(cls[1], pid))

        self.update_last_window()

        while True:
            sleep(WATCH_INTERVAL)
            self.update_active_window()
            
            if self.last_window.id == self.active_window.id:
                continue

            last_pid = self.get_window_pid(self.last_window)
            pid = self.get_window_pid(self.active_window)

            last_name, last_cls = self.get_window_name(self.last_window)
            name, cls = self.get_window_name(self.active_window)

            last_proc = self.process_by_pid(last_pid)
            #print("\t{}".format(proc.cmdline()))

            # Creation of the activity that just ended
            # TODO: Create activity upon exit
            activity = Activity(last_cls[1], self.last_selected_at, datetime.now(), cmd=last_proc.cmdline())
            self.add_activity(activity)

            print("Switched to '{}' with PID: {}".format(cls[1], pid))
            self.update_last_window()

    def get_window(self, window_id):
        return self.display.create_resource_object('window', window_id)

    def get_window_name(self, window):
        name = None
        while window:
            cls = window.get_wm_class()
            name = window.get_wm_name()
            if not cls:
                window = window.query_tree().parent
            else:
                break
        return name, cls

    def get_window_pid(self, window):
        atom = self.display.get_atom("_NET_WM_PID")
        pid_property = window.get_full_property(atom, X.AnyPropertyType)
        if pid_property:
            pid = pid_property.value[-1]
            return pid
        else:
            raise Exception("pid_property was None")

    def get_current_pid(self):
        return self.get_window_pid(active_window)

    @staticmethod
    def process_by_pid(pid):
        return psutil.Process(int(pid))
        logging.debug("Got process: " + str(p.cmdline()))
        return p


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


class ZenobaseLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(20.0)
            activities = self.flush_activities()
            # TODO: Upload to Zenobase


class CSVLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(1.0)
            activities = self.flush_activities()
            # TODO: Log to CSV


class StdOutLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(0.1)
            activities = self.flush_activities()
            for activity in activities:
                print(activity)


class Tests(unittest.TestCase):
    def test_self(self):
        process = process_by_pid(os.getpid())
        print(process)

    def test_xlib(self):
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        del sys.argv[1]
        if cmd == "test":
            unittest.main()
        else:
            print("Unknown command '{}'".format(cmd))
    else:
        x11watcher = X11Watcher()
        
        zenobaselogger = ZenobaseLogger()
        stdoutlogger = StdOutLogger()

        zenobaselogger.add_watcher(x11watcher)
        stdoutlogger.add_watcher(x11watcher)

        zenobaselogger.start()
        stdoutlogger.start()
        x11watcher.start()
