import logging
import json
import os
from time import sleep
from datetime import datetime

import pyzenobase

from base import Logger
from settings import Settings, SettingsException


class ZenobaseLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

        settings = Settings()
        if "loggers" in settings and "zenobase" in settings["loggers"]:
            self.settings = settings["loggers"]["zenobase"]
        else:
            raise SettingsException("missing entry in settings file")

        in_settings = lambda x: x in self.settings and self.settings[x]
        if not all(map(in_settings, ["username", "password", "bucket"])):
            raise SettingsException("invalid zenobase config")

    def run(self):
        while True:
            # Upload every 30 seconds
            sleep(30.0)
            activities = self.flush_activities()
            zenobase_events = map(lambda x: x.to_zenobase_event(), activities)
            # TODO: Upload to Zenobase


class JSONLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

        settings = Settings()
        if "loggers" in settings and "json" in settings["loggers"]:
            self.settings = settings["loggers"]["json"]

        if "filename" not in self.settings:
            raise SettingsException("filename wasn't defined in settings")

    def run(self):
        while True:
            sleep(3.0)
            activities = self.flush_activities()
            activities = list(map(lambda a: a.to_json_dict(), activities))

            if activities:
                # TODO: Check if file exists

                exists = os.path.exists(self.settings["filename"])
                if exists:
                    mode = "r+"
                else:
                    logging.warning("File did not exist, creating")
                    mode = "w+"

                with open(self.settings["filename"], mode) as f:
                    now = datetime.now().isoformat()
                    if not exists:
                        data = {"created": now,
                                "activities": []}
                    else:
                        data = json.load(f)
                    data["activities"].extend(activities)
                    data["updated"] = now

                    f.seek(0)
                    json.dump(data, f)
                logging.info("Saved {} activities to JSON".format(len(activities)))


class StdOutLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(0.1)
            activities = self.flush_activities()
            for activity in activities:
                print(activity)
