#!/usr/bin/python3

import os
import sys
import subprocess
import unittest
import logging
import threading
import json

import time
from time import sleep

from datetime import datetime

from loggers import *
from watchers import *


class Tests(unittest.TestCase):
    def test_self(self):
        process = process_by_pid(os.getpid())
        print(process)

    def test_xlib(self):
        pass

class Settings(dict):
    def __init__(self):
        dict.__init__(self)
        filepath = os.path.realpath(__file__)
        srcpath = os.path.dirname(filepath)
        rootpath = os.path.dirname(srcpath)
        print(rootpath)
        with open(rootpath + "/settings.json") as f:
            self.update(json.loads(f.read()))

        print("Loaded settings:")
        print("  Location: {}".format(self["location"]))
        print("  Tags: {}".format(self["tags"]))
        print("")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        del sys.argv[1]
        if cmd == "test":
            unittest.main()
        else:
            print("Unknown command '{}'".format(cmd))
    else:
        settings = Settings()

        x11watcher = X11Watcher()
        
        zenobaselogger = ZenobaseLogger()
        stdoutlogger = StdOutLogger()

        zenobaselogger.add_watcher(x11watcher)
        stdoutlogger.add_watcher(x11watcher)

        zenobaselogger.start()
        stdoutlogger.start()
        x11watcher.start()