from time import sleep
from datetime import datetime, timedelta
import logging

from pymouse import PyMouse, PyMouseEvent
from pykeyboard import PyKeyboard, PyKeyboardEvent

from ..base import Watcher, Activity


class AFKWatcher(Watcher):
    """Watches for keyboard & mouse activity and creates (not-)AFK events accordingly"""

    identifier = "afk"

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
    def is_afk(self) -> bool:
        return self._is_afk

    @is_afk.setter
    def is_afk(self, boolean: bool):
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

    def default_settings(self):
        return {"timeout": 300}


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
