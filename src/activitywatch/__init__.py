from .base import Logger, Watcher
from .modulemanager import ModuleManager
from .settings import Settings, SettingsException

from . import loggers
from . import watchers
from . import filters


def start():
    import platform
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s from %(threadName)s: %(message)s")

    # Initialize ModuleManager for the first time (it's a singleton)
    mm = ModuleManager()

    # Create Loggers
    zenobaselogger = loggers.ZenobaseLogger()
    jsonlogger = loggers.JSONLogger()
    restlogger = loggers.RestLogger()
    mongodblogger = loggers.MongoDBLogger()

    # Create Watchers
    if platform.system() == "Linux":
        windowwatcher = watchers.X11Watcher()
    #elif platform.system() == "Darwin":
    #    windowwatcher = watchers.OSXWatcher()
    else:
        raise Exception("Sorry, only Linux is currently supported, stay tuned for updates or contribute module for your operating system.")
    afkwatcher = watchers.AFKWatcher()

    # Create filters
    splitfilter = filters.SplitFilter()

    # Add loggers and watchers to ModuleManager
    mm.add_agents([zenobaselogger, jsonlogger, windowwatcher, afkwatcher, restlogger, mongodblogger, splitfilter])

    # Data from all watchers to all loggers should go through the splitfilter
    splitfilter.add_watchers(mm.watchers)
    splitfilter.add_loggers(mm.loggers)

    # Start Loggers
    mm.start_agents()
