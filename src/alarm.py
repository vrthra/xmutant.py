import signal
import logger
import os
from logger import out

# Warning, due to the way we use exceptions, any 'except:' clauses
# will catch the alarm and will not let it propagate it to where we
# want it to be. So always have a wrapping process kill over it.

class Alarm():
  class Alarm(Exception): pass

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    out().debug("enable Hook[%s]" % os.getpid())
    self.old_handler = signal.signal(signal.SIGALRM, self.raise_timeout)
    signal.alarm(self.sec)

  def __exit__(self, *args):
    out().debug("disable Hook[%s]" % os.getpid())
    signal.signal(signal.SIGALRM, self.old_handler)
    signal.alarm(0)

  def raise_timeout(self, *args):
    out().debug("throw Hook[%s]" % os.getpid())
    signal.signal(signal.SIGALRM, self.old_handler)
    signal.alarm(0)
    raise Alarm.Alarm()

