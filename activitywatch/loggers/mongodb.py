import logging
from time import sleep

import pymongo
from typing import List

from ..base import Logger, Activity


class MongoDBLogger(Logger):
    def __init__(self):
        Logger.__init__(self)
        self.client = pymongo.MongoClient()
        self.collection = self.client.activitywatch.test_collection

    def wait(self):
        self.wait_for_activities()

    def log(self, activities: List[Activity]):
        for activity in activities:
            self.collection.insert(activity.to_json_dict())
