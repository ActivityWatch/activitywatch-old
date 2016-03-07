#!/bin/python3

import threading
from time import sleep

import yappi

import activitywatch

yappi.start(profile_threads=True)

print("Starting to profile")
thread = threading.Thread(target=activitywatch.start, daemon=False)
thread.start()

try:
    sleep(60*60*24)  # Sleep for 24h, allowing activitywatch to do work
    print("Expired")
except KeyboardInterrupt:
    print("Interrupted")

yappi.stop()
print("Computing statistics, please wait...")
p = yappi.convert2pstats(yappi.get_func_stats().get())
p.sort_stats("cumtime")
p.print_stats()
