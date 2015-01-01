#!/usr/bin/python3

import logging
import threading

import time
from time import sleep

from datetime import datetime

import psutil

import Xlib
import Xlib.display
from Xlib import X, Xatom

from base import *
from loggers import *

WATCH_INTERVAL = 1.0


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
