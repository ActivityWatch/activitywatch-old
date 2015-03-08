from datetime import datetime
import json
import logging
from time import sleep
import os

from ..base import Logger
from ..settings import Settings, SettingsException


class JSONLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

        if "filename" not in self.settings:
            raise SettingsException("filename wasn't defined in settings")

        if not os.path.isabs(self.settings["filename"]):
            self.settings["filename"] = os.path.abspath(self.settings["filename"])
        logging.info("JSON logger will output to: " + self.settings["filename"])

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
                    json.dump(data, f, indent=4)
                logging.info("Saved {} activities to JSON".format(len(activities)))

    def default_settings(self):
        return {"filename": "output.json"}