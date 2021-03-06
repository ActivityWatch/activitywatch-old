import json
import os
import logging

from .utils import Singleton


DEFAULT_SETTINGS = json.dumps({
    "location": [],
    "tags": [],
    "loggers": {},
    "watchers": {}
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
                logging.warning("""Wrote default config to file,
please change the default values according to your preference. It is located in $HOME/.activitywatch.json""")
        with open(confpath) as f:
            self.update(json.loads(f.read()))

        msg = "Loaded settings"
        msg += "  Location: {}".format(self["location"])
        msg += "  Tags: {}".format(self["tags"])
        logging.info(msg)


class SettingsException(Exception):
    pass
