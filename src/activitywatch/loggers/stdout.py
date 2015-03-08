from time import sleep

from ..base import Logger


class StdOutLogger(Logger):
    def __init__(self):
        Logger.__init__(self)

    def run(self):
        while True:
            sleep(0.1)
            activities = self.flush_activities()
            for activity in activities:
                print(activity)