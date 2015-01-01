#!/usr/bin/python3

import logging
import threading
import csv

import time
from time import sleep

from datetime import datetime

import pyzenobase

from base import Logger

class ZenobaseLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(20.0)
            activities = self.flush_activities()
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
