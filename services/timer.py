from datetime import datetime, timedelta
from time import sleep
from helpers import constants


class TimerManager(object):

    @staticmethod
    def check_event(time_event, action):
        while True:
            current_time = datetime.now().strftime(constants.time_format)

            if time_event == current_time:
                print(f"send message in: {current_time}")
                action()
            else:
                print(f"current: {current_time}")

            sleep(1)
