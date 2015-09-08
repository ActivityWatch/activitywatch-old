from datetime import datetime
import json
import logging
from time import sleep
import os
from typing import List

from ..base import Logger, Activity
from ..settings import Settings, SettingsException


class JSONLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

        if "filename" not in self.settings.keys():
            raise SettingsException("filename wasn't defined in settings")

        if not os.path.isabs(self.settings["filename"]):
            self.settings["filename"] = os.path.abspath(self.settings["filename"])
        logging.info("JSON logger will output to: " + self.settings["filename"])

    def wait(self):
        sleep(30)

    def log(self, activities: List[Activity]):
        activities = list(map(lambda a: a.to_json_dict(), activities))

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
            json.dump(data, f, indent=4)
        logging.debug("Saved {} activities to JSON".format(len(activities)))

    @property
    def default_settings(self):
        return {"filename": "output.json"}
