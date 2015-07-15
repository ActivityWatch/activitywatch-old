from copy import copy
from itertools import groupby
import unittest
from datetime import datetime, timedelta
from typing import List

from activitywatch.base import Watcher, Activity, Logger
from activitywatch.settings import Settings
from activitywatch.utils import floor_datetime, ceil_datetime
from activitywatch.filters.split import split_by_interval, overlaps
from activitywatch.filters.chunk import chunk_by_tags


class MockWatcher(Watcher):
    def run(self):
        pass

    def wait(self):
        pass

    identifier = "mock"

    def __init__(self):
        settings = Settings()
        settings["watchers"][self.identifier] = {}
        Watcher.__init__(self)


class MockLogger(Logger):
    def log(self, activities: List[Activity]):
        pass

    def wait(self):
        pass

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

HOUR = timedelta(hours=1)


class SplitActivityTest(unittest.TestCase):
    def test_by_hour(self):
        dt = datetime(2015, 1, 1, 8, 30)
        td = timedelta(hours=3, minutes=23)
        activity = Activity([], dt, dt+td)

        split = split_by_interval([copy(activity), copy(activity)], interval=HOUR)
        self.assertEqual(len(split), 8)

        activity.end += -td + timedelta(minutes=2)
        split = split_by_interval([copy(activity)], interval=HOUR)
        self.assertEqual(len(split), 1)

    def test_ceil_hour(self):
        def ceil_hour(td):
            return ceil_datetime(td, td=timedelta(hours=1))

        self.assertEqual(ceil_hour(datetime(2015, 1, 1, 6, 2)), datetime(2015, 1, 1, 7))
        self.assertEqual(ceil_hour(datetime(2015, 1, 1, 6, 2)), ceil_hour(datetime(2015, 1, 1, 6, 58)))
        self.assertNotEqual(ceil_hour(datetime(2015, 1, 1, 5, 2)), ceil_hour(datetime(2015, 1, 1, 6, 4)))

    def test_floor_hour(self):
        def floor_hour(td):
            return floor_datetime(td, td=timedelta(hours=1))

        self.assertEqual(floor_hour(datetime(2015, 1, 1, 6, 2)), datetime(2015, 1, 1, 6))
        self.assertEqual(floor_hour(datetime(2015, 1, 1, 6, 2)), floor_hour(datetime(2015, 1, 1, 6, 5)))

    def test_overlaps_hour(self):
        def overlaps_hours(td):
            return overlaps(td, interval=timedelta(hours=1))

        activity = Activity([], datetime(2015, 1, 1, 5, 23), datetime(2015, 1, 1, 6, 6))
        self.assertTrue(overlaps_hours(activity))

        activity = Activity([], datetime(2015, 1, 1, 5, 23), datetime(2015, 1, 1, 6, 0, 0, 1))
        self.assertTrue(overlaps_hours(activity))

        activity = Activity([], datetime(2015, 1, 1, 6, 30), datetime(2015, 1, 1, 6, 59))
        self.assertFalse(overlaps_hours(activity))


class ChunkTest(unittest.TestCase):
    def test_chunk_by_tags(self):
        interval = timedelta(minutes=5)
        start = floor_datetime(datetime.now(), interval)

        activities = [Activity(["test"], start, start+interval*0.5),
                      Activity(["test2"], start+interval, start+interval*1.5),
                      Activity(["test"], start+interval*2, start+interval*2.5)]
        self.assertEqual(3, len(activities))

        activities.append(Activity(["test"], start+interval, start+interval*1.5))
        self.assertEqual(4, len(activities))

        self.assertEqual(2, len(chunk_by_tags(activities)))
