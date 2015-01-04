import sys
import unittest

from loggers import *
from settings import Settings
from watchers import *


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
        settings = Settings()

        # Create Loggers
        zenobaselogger = ZenobaseLogger()
        jsonlogger = JSONLogger()

        # Create Watchers
        x11watcher = X11Watcher()

        # Add Watchers to loggers
        zenobaselogger.add_watcher(x11watcher)
        jsonlogger.add_watcher(x11watcher)

        # Start Loggers
        zenobaselogger.start()
        jsonlogger.start()

        # Start Watchers
        x11watcher.start()
