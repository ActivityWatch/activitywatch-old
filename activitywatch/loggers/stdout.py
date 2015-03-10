from time import sleep
from typing import List

from ..base import Logger, Activity


class StdOutLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def wait(self):
        self.wait_for_activities()

    def log(self, activities: List[Activity]):
        for activity in activities:
            print(activity)