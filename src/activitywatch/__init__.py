from .base import Logger, Watcher
from .modulemanager import ModuleManager
from .settings import Settings, SettingsException

from . import loggers
from . import watchers


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
    elif platform.system() == "Darwin":
        windowwatcher = watchers.OSXWatcher()
    else:
        raise Exception("Sorry, only Linux is currently supported, stay tuned for updates or contribute module for your operating system.")
    afkwatcher = watchers.AFKWatcher()

    # Add loggers and watchers to ModuleManager
    mm.add_agents([zenobaselogger, jsonlogger, windowwatcher, afkwatcher, restlogger, mongodblogger])

    # Connect watchers to loggers
    zenobaselogger.add_watchers(mm.watchers)
    jsonlogger.add_watchers(mm.watchers)
    mongodblogger.add_watchers(mm.watchers)

    # Start Loggers
    mm.start_agents()
