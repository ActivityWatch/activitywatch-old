import unittest
from datetime import datetime, timedelta

from activitywatch.base import Watcher, Activity, Logger
from activitywatch.settings import Settings


class MockWatcher(Watcher):
    def __init__(self):
        settings = Settings()
        settings["watchers"]["mock"] = {}
        Watcher.__init__(self, "mock")


class MockLogger(Logger):
    def __init__(self):
        settings = Settings()
        settings["loggers"]["mock"] = {}
        Logger.__init__(self, "mock")


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


class ActivityTest(unittest.TestCase):
    def test_to_zenobase(self):
        TAG = "something"
        activity = Activity(TAG, started_at=datetime.now(), ended_at=datetime.now())
        event = activity.to_zenobase_event()
        self.assertTrue(event["tag"] == TAG)


class SettingsTest(unittest.TestCase):
    def test_instance(self):
        self.assertIs(Settings(), Settings())


