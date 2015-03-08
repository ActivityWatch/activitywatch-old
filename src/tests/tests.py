from copy import copy
from itertools import groupby
import unittest
from datetime import datetime, timedelta
from activitywatch.filters.split import floor_hour, ceil_hour, split_by_hour, overlaps_hours

from activitywatch.base import Watcher, Activity, Logger
from activitywatch.settings import Settings


class MockWatcher(Watcher):
    identifier = "mock"

    def __init__(self):
        settings = Settings()
        settings["watchers"][self.identifier] = {}
        Watcher.__init__(self)


class MockLogger(Logger):
    identifier = "mock"

    def __init__(self):
        settings = Settings()
        settings["loggers"][self.identifier] = {}
        Logger.__init__(self)


class LoggerWatcherTest(unittest.TestCase):
    def test_activity_flow(self):
        watcher = MockWatcher()
        logger = MockLogger()
        logger.add_watcher(watcher)

        watcher.dispatch_activity(Activity("test", datetime.now()-timedelta(days=1), datetime.now()))

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



class SplitActivityTest(unittest.TestCase):
    def test_by_hour(self):
        dt = datetime(2015, 1, 1, 8, 30)
        td = timedelta(hours=3, minutes=23)
        activity = Activity([], dt, dt+td)

        split = split_by_hour([copy(activity), copy(activity)])
        self.assertEquals(len(split), 8)

        split = split_by_hour([Activity([], dt, dt+timedelta(minutes=2))])
        self.assertEquals(len(split), 1)

    def test_ceil_hour(self):
        self.assertEquals(ceil_hour(datetime(2015, 1, 1, 6, 2)), datetime(2015, 1, 1, 7))
        self.assertEquals(ceil_hour(datetime(2015, 1, 1, 6, 2)), ceil_hour(datetime(2015, 1, 1, 6, 58)))
        self.assertNotEquals(ceil_hour(datetime(2015, 1, 1, 5, 2)), ceil_hour(datetime(2015, 1, 1, 6, 4)))

    def test_floor_hour(self):
        self.assertEquals(floor_hour(datetime(2015, 1, 1, 6, 2)), datetime(2015, 1, 1, 6))
        self.assertEquals(floor_hour(datetime(2015, 1, 1, 6, 2)), floor_hour(datetime(2015, 1, 1, 6, 5)))

    def test_overlaps_hour(self):
        activity = Activity([], datetime(2015, 1, 1, 5, 23), datetime(2015, 1, 1, 6, 6))
        self.assertTrue(overlaps_hours(activity))

        activity = Activity([], datetime(2015, 1, 1, 5, 23), datetime(2015, 1, 1, 6, 0, 0, 1))
        self.assertTrue(overlaps_hours(activity))

        activity = Activity([], datetime(2015, 1, 1, 6, 30), datetime(2015, 1, 1, 6, 59))
        self.assertFalse(overlaps_hours(activity))
