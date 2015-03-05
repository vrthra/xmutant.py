import doctest
import alarm
import os
import config
from logger import out

def pr(v):
  out().debug(v)
  return True

def runAllTests(module, msg):
  finder = doctest.DocTestFinder(exclude_empty=False)
  runner = doctest.DocTestRunner(verbose=False)
  for test in finder.find(module, module.__name__):
    try:
      out().debug("Test M[%s] ->%s  %s:%s (%s)" % (os.getpid(), test.name, test.filename, test.lineno, msg))
      with alarm.Alarm(config.t['WaitTestRun']):
        runner.run(test, out=pr)
      out().debug("Test M[%s] <-%s failed:%s/%s (%s)" % (os.getpid(), test.name, runner.failures, runner.tries, msg))
    except alarm.Alarm.Alarm:
      out().debug("Test M[%s] #-%s %s" % (os.getpid(), test.name, msg))
      return False # timeout!
    if runner.failures > 0: return False
  return True
