import schedule
import time

from src.run import Execution
from src.settings import settings

exe = Execution()

class Control:

    def __init__(self) -> None:
        self.interval = settings.get_interval()
        self.stop = False

    def job(self) -> None:
        exe.running()

    def check_interval(self) -> None:
        interval = settings.get_interval()

        if self.interval != interval:
            self.interval = interval
            self.stop = True
            self.doing()

    def doing(self) -> None:
        schedule.every(1).minutes.do(self.check_interval)
        schedule.every(self.interval).minutes.do(self.job)

        while True:
            schedule.run_pending()
            time.sleep(1)

            if self.stop:
                self.stop = False
                break