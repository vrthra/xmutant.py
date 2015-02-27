import doctest
import alarm
import os
import config
from logger import out

def runAllTests(module):
  finder = doctest.DocTestFinder(exclude_empty=False)
  runner = doctest.DocTestRunner(verbose=False)
  for test in finder.find(module, module.__name__):
    try:
      out().debug("Test M[%s] >%s" % (os.getpid(), test.name))
      with alarm.Alarm(config.WaitTestRun):
        runner.run(test, out=lambda x: True)
      out().debug("Test M[%s] <%s" % (os.getpid(), test.name))
    except alarm.Alarm.Alarm:
      out().debug("Test M[%s] #%s" % (os.getpid(), test.name))
      return True # timeout!
    if runner.failures > 0: return True
  return False
