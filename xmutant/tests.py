import doctest
import alarm
import config

def pr(v):
    return True


def runAllTests(module, msg):
    finder = doctest.DocTestFinder(exclude_empty=False)
    runner = doctest.DocTestRunner(verbose=False)
    for test in finder.find(module, module.__name__):
        try:
            with alarm.Alarm(config.t['WaitTestRun']):
                runner.run(test, out=pr)
        except alarm.Alarm.Alarm:
            return False  # timeout!
        if runner.failures > 0: return False
    return True
