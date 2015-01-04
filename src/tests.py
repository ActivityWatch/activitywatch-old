import unittest
from datetime import datetime, timedelta

from base import Watcher, Activity, Logger


class MockWatcher(Watcher):
    def __init__(self):
        Watcher.__init__(self)


class MockLogger(Logger):
    def __init__(self):
        Logger.__init__(self)


class LoggerWatcherTest(unittest.TestCase):
    def test_activity_flow(self):
        watcher = MockWatcher()
        logger = MockLogger()
        logger.add_watcher(watcher)

        watcher.add_activity(Activity("test", datetime.now()-timedelta(days=1), datetime.now()))

        activities = logger.flush_activities()
        self.assertTrue(len(activities) == 1)

        activities = logger.flush_activities()
        self.assertTrue(len(activities) == 0)
