import sys
import unittest

from loggers import *
from settings import Settings
from watchers import *


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s from %(threadName)s: %(message)s")

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        del sys.argv[1]
        if cmd == "test":
            unittest.main()
        else:
            print("Unknown command '{}'".format(cmd))
    else:
        settings = Settings()

        # Create Loggers
        zenobaselogger = ZenobaseLogger()
        jsonlogger = JSONLogger()

        # Create Watchers
        x11watcher = X11Watcher()
        afkwatcher = AFKWatcher()

        # Add Watchers to loggers
        zenobaselogger.add_watcher(x11watcher)
        jsonlogger.add_watcher(x11watcher)
        zenobaselogger.add_watcher(afkwatcher)
        jsonlogger.add_watcher(afkwatcher)

        # Start Loggers
        zenobaselogger.start()
        jsonlogger.start()

        # Start Watchers
        x11watcher.start()
        afkwatcher.start()
