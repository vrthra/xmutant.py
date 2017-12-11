import signal
import logger
from logger import out


# Warning, due to the way we use exceptions, any 'except:' clauses
# will catch the alarm and will not let it propagate it to where we
# want it to be. So always have a wrapping process kill over it.

class Alarm():
    class Alarm(Exception): pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        self.old_handler = signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)
        signal.signal(signal.SIGALRM, self.old_handler)

    def raise_timeout(self, *args):
        # hacky, set a timeout for 1 sec. and ensure
        # to disable it later.
        signal.alarm(1)
        raise Alarm.Alarm()
