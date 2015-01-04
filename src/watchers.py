#!/usr/bin/python3

from time import sleep

from datetime import datetime, timedelta

import psutil

import Xlib
import Xlib.display
from Xlib import X, Xatom

from pymouse import PyMouse
from pykeyboard import PyKeyboard

from base import Watcher, Activity

WATCH_INTERVAL = 0.5


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
        window = self.get_window(w_id)

        try:
            self.get_window_pid(window)
        except Xlib.error.BadWindow:
            print("Error while updating active window, trying again.")
            sleep(0.1)
            self.update_active_window()
            return

        self._active_window = window

    def run(self):
        self.update_active_window()
        window = self.active_window
        
        name, cls = self.get_window_name(window)
        pid = self.get_window_pid(window)
        process = self.process_by_pid(pid)
        print("First focus is '{}' with PID: {}".format(cls[1], pid))

        self.update_last_window()

        while True:
            sleep(WATCH_INTERVAL)
            self.update_active_window()
            
            if self.last_window.id == self.active_window.id:
                continue

            last_pid = pid
            pid = self.get_window_pid(self.active_window)

            last_name, last_cls = name, cls
            name, cls = self.get_window_name(self.active_window)

            last_process = process
            process = self.process_by_pid(last_pid)

            # Creation of the activity that just ended
            # TODO: Create activity upon exit
            activity = Activity(last_cls[1], self.last_selected_at, datetime.now(), cmd=last_process.cmdline())
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
            # TODO: Needed?
            raise Exception("pid_property was None")

    def get_current_pid(self):
        return self.get_window_pid(self.active_window)

    @staticmethod
    def process_by_pid(pid):
        return psutil.Process(int(pid))


class AFKWatcher(Watcher):
    """Watches for keyboard & mouse activity and creates (not-)AFK events accordingly"""

    def __init__(self):
        # TODO: Use MouseEvent and KeyboardEvent instead
        # TODO: Detect keyboard usage
        # TODO: (nice to have) Xbox 360 controller usage
        Watcher.__init__(self)
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

        self.last_activity = None
        self.now = None

        self._is_afk = True
        self.afk_changed = datetime.now()

    @property
    def is_afk(self):
        return self._is_afk

    @is_afk.setter
    def is_afk(self, boolean):
        if self._is_afk == boolean:
            print("Tried to set to what already was")
            return

        self.add_activity(Activity([("non-" if boolean else "")+"AFK"], self.afk_changed, self.now))

        self._is_afk = boolean
        self.afk_changed = datetime.now()
        print("Is " + ("now" if boolean else "no longer") + " AFK")

    def run(self):
        self.last_activity = datetime.now()
        last_position = None

        while True:
            sleep(0.1)

            self.now = datetime.now()
            position = self.mouse.position()

            passed_time = self.now - self.last_activity
            passed_afk = passed_time > timedelta(seconds=5)

            # If mouse moved
            if position != last_position:
                if self.is_afk and not passed_afk:
                    self.is_afk = False

                self.last_activity = self.now
                last_position = position
            # If mouse didn't move
            else:
                if not self.is_afk and passed_afk:
                    self.is_afk = True

