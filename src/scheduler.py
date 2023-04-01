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

    def tick(self, run):
        print("running tick")

        try:
            run()

            print("tick finished")
        except Exception as e:
            print(f"tick error: {e}")

        time.sleep(self.interval_seconds)

        self.tick(run)
