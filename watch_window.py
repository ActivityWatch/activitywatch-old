#!/usr/bin/python3

#####################
#  Stdlib Packages  #
#####################

import os
import sys
import subprocess
import unittest
import logging

import time
from time import sleep

from datetime import datetime

#####################
# External packages #
#####################

import psutil

import Xlib
import Xlib.display
from Xlib import X, Xatom

display = Xlib.display.Display()
screen = display.screen()

def main():
    window_id = None
    selected_at = datetime.now()
    while True:
        sleep(1.0)
        atom = display.get_atom("_NET_ACTIVE_WINDOW")
        property = screen.root.get_full_property(atom, X.AnyPropertyType)
        
        # Skip if same as before
        if window_id == property.value[0]:
            continue

        # New window has been focused
        # Add actions such as log to local db here
        print("Window selected for: {}\n".format(datetime.now() - selected_at))
        selected_at = datetime.now()

        window_id = property.value[0]
        window = get_window(window_id)
        
        property = window.get_full_property(display.get_atom("_NET_WM_PID"), X.AnyPropertyType)
        pid = property.value[-1]

        proc = process_by_pid(pid)
        name, cls = get_window_name(window)
        print("Switched to '{}' with PID: {}".format(cls[1], pid))
        print("\t{}".format(proc.cmdline()))

def get_window_name(window):
    name = None
    while window:
        cls = window.get_wm_class()
        name = window.get_wm_name()
        if not cls:
            window = window.query_tree().parent
        else:
            break
    return name, cls

def get_window(window_id):
    return display.create_resource_object('window', window_id)

def process_by_pid(pid):
    p = psutil.Process(int(pid))
    logging.debug("Got process: " + str(p.cmdline()))
    return p


class Tests(unittest.TestCase):
    def test_self(self):
        process = process_by_pid(os.getpid())
        print(process)

    def test_xlib(self):
        pass
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        del sys.argv[1]
        if cmd == "test":
            unittest.main()
        elif cmd == "":
            pass
        else:
            print("Unknown command '{}'".format(cmd))
    else:
        main()
