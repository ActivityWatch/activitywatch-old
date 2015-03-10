import logging
from copy import copy
from datetime import datetime, timedelta
from time import sleep
from typing import Iterable, List

from ..base import Filter, Activity
from ..utils import floor_datetime, ceil_datetime


def overlaps(activity: Activity, interval: timedelta) -> bool:
    return floor_datetime(activity.start, interval) != floor_datetime(activity.end, interval)


def split_by_interval(activities: List[Activity], interval: timedelta) -> List[Activity]:
    """
    Splits activities that have a duration spanning more
    than one of the segments defined by td.
    """
    non_overlapping = list(filter(lambda x: not overlaps(x, interval), activities))
    overlapping = filter(lambda act: overlaps(act, interval), activities)

    for activity in overlapping:
        while overlaps(activity, interval):
            separator_hour = ceil_datetime(activity.start, interval)
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

    def wait(self):
        self.wait_for_activities()

    def process(self, activities: List[Activity]) -> List[Activity]:
        # load interval/td from settings
        return split_by_interval(activities, interval=timedelta(hours=1))
