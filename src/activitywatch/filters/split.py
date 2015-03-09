import logging
from copy import copy
from datetime import datetime, timedelta
from time import sleep
from ..base import Filter


def time_to_next_hour(now=datetime.now()) -> timedelta:
    return next_hour(now) - now


def next_hour(now=datetime.now()) -> datetime:
    return hour_history(1, now)


def hour_history(offset: int, now: datetime=datetime.now()) -> datetime:
    return floor_hour(now) + timedelta(hours=offset)


def floor_hour(dt: datetime) -> datetime:
    return datetime(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour)


def ceil_hour(dt: datetime) -> datetime:
    return floor_hour(dt) + timedelta(hours=1)


def overlaps_hours(activity) -> bool:
    return floor_hour(activity.start) != floor_hour(activity.end)


def split_by_hour(activities) -> "list[Activity]":
    non_overlapping = list(filter(lambda x: not overlaps_hours(x), activities))
    overlapping = filter(overlaps_hours, activities)

    for activity in overlapping:
        while overlaps_hours(activity):
            separator_hour = ceil_hour(activity.start)
            non_overlapping_activity = copy(activity)
            non_overlapping_activity.end = separator_hour
            non_overlapping.append(non_overlapping_activity)
            activity.start = separator_hour
        non_overlapping.append(activity)

    return non_overlapping


class SplitFilter(Filter):
    """
    Takes all data that overlaps and splits it
    """

    def run(self):
        while True:
            sleep(10)
            activities = split_by_hour(self.flush_activities())
            if len(activities) == 0:
                continue
            self.dispatch_activities(activities)
            logging.info("SplitFilter dispatched {} activities".format(len(activities)))
