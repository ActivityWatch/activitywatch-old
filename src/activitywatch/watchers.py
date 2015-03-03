from time import sleep
from datetime import datetime, timedelta
import logging

import psutil

import Xlib
import Xlib.display
from Xlib import X, Xatom

from pymouse import PyMouse, PyMouseEvent
from pykeyboard import PyKeyboard, PyKeyboardEvent

from .base import Watcher, Activity


class X11Watcher(Watcher):
    """Watches activity in X11"""
    # TODO: Move window helper functions to container class for xlib's Window

    NAME = "x11"

    def __init__(self):
        Watcher.__init__(self)
        self.display = Xlib.display.Display()
        self.screen = self.display.screen()

        self._last_window = None
        self._active_window = None

        self.window_name = None
        self.pid = None
        self.cls = None
        self.process = None
        self.selected_at = None

        self.last_name = None
        self.last_pid = None
        self.last_cls = None
        self.last_process = None
        self.last_selected_at = None

    @property
    def last_window(self):
        return self._last_window

    def update_last_window(self):
        self._last_window = self.active_window
        self.last_selected_at = self.selected_at
        self.last_pid = self.pid
        self.last_name, self.last_cls = self.window_name, self.cls
        self.last_process = self.process

    @property
    def active_window(self):
        return self._active_window

    def update_active_window(self) -> bool:
        """Updates the active window and stores its properties

        Returns True if changed, False if was unchanged"""

        atom = self.display.get_atom("_NET_ACTIVE_WINDOW")
        window_prop = self.screen.root.get_full_property(atom, X.AnyPropertyType)
        window_id = window_prop.value[-1]
        window = self.get_window(window_id)

        if not self.last_window is None:
            # Was not the first window
            if self.last_window.id == window_id:
                # If window was same as last
                return False

        try:
            self.get_window_pid(window)
        except Xlib.error.BadWindow:
            logging.error("Error while updating active window, trying again.")
            sleep(0.1)
            return False

        self.pid = self.get_window_pid(window)
        self.window_name, self.cls = self.get_window_name(window)
        self.process = self.process_by_pid(self.pid)
        self.cmd = self.process.cmdline()
        self.selected_at = datetime.now()

        self._active_window = window

        return True

    def run(self):
        success = False
        while not success:
            success = self.update_active_window()

        logging.info("First focus is '{}'".format(self.window_name))

        self.update_last_window()

        while True:
            # TODO: Make sleep interval a setting
            sleep(0.1)
            try:
                self.loop()
            except Exception as e:
                logging.error("Exception was thrown while running loop: '{}', trying again.".format(e))
                continue

    def loop(self):
        changed = self.update_active_window()
        if not changed:
            return

        # Creation of the activity that just ended
        # TODO: Create activity upon exit
        activity = Activity(self.last_cls, self.last_selected_at, datetime.now(), cmd=self.cmd)
        self.add_activity(activity)

        logging.info("Switched to '{}' with PID: {}".format(self.cls, self.pid))

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

    NAME = "afk"

    def __init__(self):
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
        if boolean is False:
            self.last_activity = self.now

        if self._is_afk == boolean:
            logging.debug("Tried to set to what already was")
            return

        self.add_activity(Activity([("non-" if boolean else "")+"AFK"], self.afk_changed, self.now))

        self._is_afk = boolean
        self.afk_changed = datetime.now()
        logging.info("Is " + ("now" if boolean else "no longer") + " AFK")

    def run(self):
        self.now = datetime.now()
        self.last_activity = datetime.now()
        KeyboardListener(self).start()
        MouseListener(self).start()

        while True:
            sleep(1.0)
            self.now = datetime.now()

            passed_time = self.now - self.last_activity
            passed_afk = passed_time > timedelta(seconds=self.settings["timeout"])

            if not self.is_afk and passed_afk:
                self.is_afk = True


class KeyboardListener(PyKeyboardEvent):
    def __init__(self, watcher):
        PyKeyboardEvent.__init__(self)
        self.watcher = watcher

    def tap(self, keycode, character, press):
        logging.debug("Tapped key: {}".format(keycode))
        self.watcher.is_afk = False


class MouseListener(PyMouseEvent):
    def __init__(self, watcher):
        PyMouseEvent.__init__(self)
        self.watcher = watcher

    def click(self, x, y, button, press):
        logging.debug("Clicked mousebutton: {}".format(button))
        self.watcher.is_afk = False

    def move(self, x, y):
        logging.debug("Moved mouse to: {},{}".format(x, y))
        self.watcher.is_afk = False
