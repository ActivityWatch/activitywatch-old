#!/usr/bin/python3

try:
    import activitywatch
except ImportError:
    raise ImportError("Could not import the activitywatch module, please install it with pip3 before running.")

if __name__ == "__main__":
    activitywatch.start()