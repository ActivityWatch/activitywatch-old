from itertools import groupby
from activitywatch.utils import ceil_datetime
from functools import reduce
import logging
import unittest
from copy import copy
from datetime import datetime, timedelta
from time import sleep
from typing import Iterable, List

from ..base import Filter, Activity


def _sum_duration(x, y):
    return x + y.duration


def chunk_by_tags(activities: List[Activity]) -> List[Activity]:
    key_function = lambda x: tuple(x.tags)
    result_activities = []  # type: List[Activity]
    data = sorted(activities, key=key_function)
    for key, group in groupby(data, key_function):
        group = list(group)
        duration = reduce(_sum_duration, group, timedelta(seconds=0))
        start = sorted(group, key=lambda x: x.start)[0]
        result_activities.append(Activity(start.tags, started_at=start.start, ended_at=start.end + (duration - start.duration)))
    return result_activities


class ChunkFilter(Filter):
    """
    Takes all data that overlaps and splits it
    """
    # TODO: Automatically split on interval as well?

    def wait(self):
        now = datetime.now()
        seconds_to_next_batch = (ceil_datetime(now, self.interval)-now).total_seconds()
        sleep(seconds_to_next_batch)

    def process(self, activities: List[Activity]) -> List[Activity]:
        return chunk_by_tags(activities)

    @property
    def interval(self) -> timedelta:
        return timedelta(seconds=self.settings["interval"])
