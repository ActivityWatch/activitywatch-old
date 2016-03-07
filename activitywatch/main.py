import logging

from . import loggers, watchers, filters
from . import ModuleManager
from . import rest

def start(loglevel=logging.INFO):
    import platform
    import argparse

    parser = argparse.ArgumentParser(description='Logs your computer activities and much more. Built to be extended.')
    parser.add_argument('--debug', action='store_true', help='Enables logging of debug messages')
    #parser.add_argument('--profile', action='store_true', help='Enables profiling for use in performance optimization')
    args = parser.parse_args()

    #if args.profile:
    #    import yappi
    #    yappi.start()

    if args.debug:
        loglevel = logging.DEBUG

    logging.basicConfig(level=loglevel, format="%(asctime)s %(levelname)s from %(threadName)s: %(message)s")

    # Initialize ModuleManager for the first time (it's a singleton)
    mm = ModuleManager()

    # Create Loggers
    jsonlogger = loggers.JSONLogger()
    #zenobaselogger = loggers.ZenobaseLogger()
    #mongodblogger = loggers.MongoDBLogger()

    # Create Watchers
    if platform.system() == "Linux":
        windowwatcher = watchers.X11Watcher()
    elif platform.system() == "Darwin":
        windowwatcher = watchers.OSXWatcher()
    else:
        raise Exception("""Sorry, your operating system is not currently supported,
                           you can stay tuned for updates or contribute support for your operating system by
                           searching for your operating system in the issue tracker.""")
    afkwatcher = watchers.AFKWatcher()

    # Create filters
    splitfilter = filters.SplitFilter()

    # Add loggers and watchers to ModuleManager
    mm.add_agents([jsonlogger, windowwatcher, splitfilter, afkwatcher])

    # Data from all watchers to all loggers should go through the splitfilter
    splitfilter.add_watchers(mm.watchers)
    splitfilter.add_loggers(mm.loggers)

    # Start Loggers
    mm.start_agents()

    try:
        from . import gui
        gui.main()
    except ImportError:
        # PyQt4 will fail import if not installed
        logging.info("PyQt4 not available, running without trayicon")
        pass

    rest.start_server()
