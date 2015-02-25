import signal
import logger
import os
from logger import out

class Alarm():
  class Alarm(Exception): pass

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    out().debug("+Hook[%s]" % os.getpid())
    signal.signal(signal.SIGALRM, self.raise_timeout)
    signal.alarm(self.sec)

  def __exit__(self, *args):
    out().debug("-Hook[%s]" % os.getpid())
    signal.alarm(0)

  def raise_timeout(self, *args):
    out().debug("*Hook[%s]" % os.getpid())
    raise Alarm.Alarm()

