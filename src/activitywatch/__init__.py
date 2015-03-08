from .base import Logger, Watcher
from .modulemanager import ModuleManager
from .settings import Settings, SettingsException

from . import loggers
from . import watchers


def start():
    import sys
    import platform
    import unittest
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s from %(threadName)s: %(message)s")

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        del sys.argv[1]
        if cmd == "test":
            unittest.main()
        else:
            print("Unknown command '{}'".format(cmd))
    else:
        settings = Settings()


        mm = ModuleManager()
        # Create Loggers
        zenobaselogger = loggers.ZenobaseLogger()
        jsonlogger = loggers.JSONLogger()

        # Create Watchers
        if platform.system() == "Linux":
            windowwatcher = watchers.X11Watcher()
        elif platform.system() == "Darwin":
            windowwatcher = watchers.OSXWatcher()
        else:
            raise Exception("Sorry, only Linux is currently supported, stay tuned for updates or contribute module for your operating system.")
        afkwatcher = watchers.AFKWatcher()

        # Add Watchers to loggers
        zenobaselogger.add_watcher(windowwatcher)
        jsonlogger.add_watcher(windowwatcher)
        zenobaselogger.add_watcher(afkwatcher)
        jsonlogger.add_watcher(afkwatcher)

        # Add loggers and watchers to ModuleManager
        mm.add_agent(zenobaselogger)
        mm.add_agent(jsonlogger)
        mm.add_agent(windowwatcher)
        mm.add_agent(afkwatcher)

        mm.add_agent(loggers.RestLogger())

        # Start Loggers
        mm.start_agents()
