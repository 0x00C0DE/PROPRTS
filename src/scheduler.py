import sys
import time

class Scheduler:
    should_run: bool = False
    interval_seconds: int = 60
    run = None

    def __init__(self):
        self.get_args()
    def get_args(self):
        if len(sys.argv) == 3:
            self.should_run = True if sys.argv[1] else False
            self.interval_seconds = float(sys.argv[2])
    def start(self, run):
        run()

        time.sleep(self.interval_seconds)

        self.start(run)



