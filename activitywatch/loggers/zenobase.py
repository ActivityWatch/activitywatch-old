import logging
from time import sleep
import pyzenobase
from typing import List

from ..base import Logger, Activity
from ..settings import SettingsException


class ZenobaseLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

        if not self.settings["username"] or not self.settings["password"]:
            raise SettingsException("username or password was empty in settings")

        self.api = pyzenobase.ZenobaseAPI(self.settings["username"], self.settings["password"])
        self.bucket_id = self.api.create_or_get_bucket(self.settings["bucket"])["@id"]

    def wait(self):
        sleep(60)

    def log(self, activities: List[Activity]):
        zenobase_events = list(map(lambda x: x.to_zenobase_event(), activities))
        self.api.create_events(self.bucket_id, zenobase_events)

    def default_settings(self):
        return {
            "bucket": "ActivityWatch",
            "username": "",
            "password": ""
        }
