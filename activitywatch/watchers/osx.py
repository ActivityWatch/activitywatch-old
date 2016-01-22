import logging

from AppKit import NSWorkspace

from ..base import Watcher


class OSXWatcher(Watcher):
    identifier = "osx"

    def run(self):
        logging.warning("OS X Window-watcher not implemented")
        return

