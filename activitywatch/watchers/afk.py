import platform
from threading import Event, Thread
from datetime import datetime, timedelta
import logging

from pymouse import PyMouse, PyMouseEvent
from pykeyboard import PyKeyboard, PyKeyboardEvent

from ..base import Watcher, Activity


def _repeat_trigger(waiter: Event, trigger: Event, timeout):
    if waiter.wait(timeout+1):
        trigger.set()


def _wait_for_either(a: Event, b: Event, timeout=None):
    """Waits for any one of two events to happen"""
    # TODO: Reuse threads, don't recreate
    trigger = Event()
    ta = Thread(target=_repeat_trigger, args=(a, trigger, timeout))
    tb = Thread(target=_repeat_trigger, args=(b, trigger, timeout))
    ta.start()
    tb.start()
    # Now do the union waiting
    return trigger.wait(timeout)


class AFKWatcher(Watcher):
    """Watches for keyboard & mouse activity and creates (not-)AFK events accordingly"""

    identifier = "afk"

    def __init__(self):
        # TODO: (nice to have) Xbox 360 controller usage
        Watcher.__init__(self)
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

        self.last_activity = None
        self.now = datetime.now()

        self._is_afk = True
        self.afk_state_last_changed = datetime.now()

    @property
    def is_afk(self) -> bool:
        return self._is_afk

    @is_afk.setter
    def is_afk(self, is_now_afk: bool):
        if self._is_afk == is_now_afk:
            logging.debug("Tried to set to what already was, this shouldn't happen")
            return

        self._is_afk = is_now_afk
        logging.debug("Is " + ("now" if is_now_afk else "no longer") + " AFK")

        end_event = self.last_activity if is_now_afk else self.now
        self.dispatch_activity(Activity([("non-AFK" if is_now_afk else "AFK")], self.afk_state_last_changed, end_event))
        self.afk_state_last_changed = end_event

    def run(self):
        self.now = datetime.now()
        self.last_activity = self.now
        self.afk_state_last_changed = self.now

        keyboard_activity_event = Event()
        mouse_activity_event = Event()

        # OS X doesn't seem to like the KeyboardListener... segfaults
        if platform.system() != "Darwin":
            KeyboardListener(keyboard_activity_event).start()
        else:
            logging.warning("KeyboardListener is broken in OS X, will not use for detecting AFK state.")
        MouseListener(mouse_activity_event).start()

        while True:
            if _wait_for_either(keyboard_activity_event, mouse_activity_event, timeout=1):
                # Check if there has been any activity on the mouse or keyboard and if so,
                # update last_activity to now and set is_afk to False if previously AFK
                self.now = datetime.now()
                if self.is_afk:
                    # If previously AFK, keyboard/mouse activity now indicates the user isn't AFK
                    self.is_afk = False
                self.last_activity = self.now
                keyboard_activity_event.clear()
                mouse_activity_event.clear()

            if not self.is_afk:
                # If not previously AFK, check if enough time has passed for it to now count as AFK
                self.now = datetime.now()
                passed_time = self.now - self.last_activity
                passed_afk = passed_time > timedelta(seconds=self.settings["timeout"])
                if passed_afk:
                    self.is_afk = True


    @property
    def default_settings(self):
        return {"timeout": 300}


class KeyboardListener(PyKeyboardEvent):
    def __init__(self, keyboard_activity_event):
        PyKeyboardEvent.__init__(self)
        self.keyboard_activity_event = keyboard_activity_event

    def tap(self, keycode, character, press):
        #logging.debug("Clicked keycode: {}".format(keycode))
        self.keyboard_activity_event.set()


class MouseListener(PyMouseEvent):
    def __init__(self, mouse_activity_event):
        PyMouseEvent.__init__(self)
        self.mouse_activity_event = mouse_activity_event

    def click(self, x, y, button, press):
        #logging.debug("Clicked mousebutton: {}".format(button))
        self.mouse_activity_event.set()

    def move(self, x, y):
        #logging.debug("Moved mouse to: {},{}".format(x, y))
        self.mouse_activity_event.set()
