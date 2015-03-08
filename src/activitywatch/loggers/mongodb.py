import logging
from time import sleep

import pymongo

from ..base import Logger


class MongoDBLogger(Logger):
    def __init__(self):
        Logger.__init__(self)
        self.client = pymongo.MongoClient()
        self.collection = self.client.activitywatch.test_collection

    def run(self):
        while True:
            sleep(10)
            activities = self.flush_activities()
            if len(activities) == 0:
                continue
            for activity in activities:
                self.collection.insert(activity.to_json_dict())
            logging.info("Logged {} activities to MongoDB".format(len(activities)))


