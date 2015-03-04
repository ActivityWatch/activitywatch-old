import json
import os
import logging

from .utils import Singleton


DEFAULT_SETTINGS = json.dumps({
    "location": [],
    "tags": [],
    "loggers": {
        "zenobase": {
            "bucket": "ActivityWatch",
            "username": "FILL ME IN",
            "password": "FILL ME IN"
        },
        "json": {
            "filename": "output.json"
        }
    },
    "watchers": {
        "x11": {},
        "afk": {
            "timeout": 300
        }
    }
}, indent=4)


@Singleton
class Settings(dict):
    def __init__(self):
        # TODO: If settingsfile doesn't exist, create one from default settings file
        # TODO: Store in users application data folder
        dict.__init__(self)
        confdir = os.getenv("HOME")
        confpath = confdir + "/.activitywatch.json"
        if not os.path.exists(confpath):
            with open(confpath, "w+") as f:
                f.write(DEFAULT_SETTINGS)
        with open(confpath) as f:
            self.update(json.loads(f.read()))

        msg = "Loaded settings"
        msg += "  Location: {}".format(self["location"])
        msg += "  Tags: {}".format(self["tags"])
        logging.info(msg)


class SettingsException(Exception):
    pass
