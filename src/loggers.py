#!/usr/bin/python3

from time import sleep

import pyzenobase

from base import Logger


class ZenobaseLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            # Upload every 30 seconds
            sleep(30.0)
            activities = self.flush_activities()
            zenobase_events = map(lambda x: x.to_zenobase_event(), activities)
            # TODO: Upload to Zenobase


class CSVLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(1.0)
            activities = self.flush_activities()
            # TODO: Log to CSV


class StdOutLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(0.1)
            activities = self.flush_activities()
            for activity in activities:
                print(activity)
