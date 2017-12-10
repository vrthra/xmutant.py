# Make sure that WaitSingleMutant is a sane value. the WaitSingleFn is overly
# optimistic and fails to handle cases where we have exception handlers that
# are overly aggressive with 'except:' -- the sigalarm we use gets stuck in
# these exception handlers.
WaitSingleFn = 1
WaitTestRun = 10 * WaitSingleFn
WaitSingleMutant = 1000 * WaitSingleFn
MaxTries = 10000
MaxSpace = 1000000
MaxListSpace = 7
NPool = 0

FnTimedOut = 0
FnDetected = 1
FnNotEq = 2
FnProbEq = 3

TerminateTimedoutMutants = False

t = dict()
t['WaitSingleFn'] = WaitSingleFn
t['WaitTestRun'] = WaitTestRun
t['WaitSingleMutant'] = WaitSingleMutant

config = dict()
config['MaxSpace'] = MaxSpace
config['MaxTries'] = MaxTries
config['Timeout'] = "%s,%s,%s" % (WaitSingleFn, WaitTestRun, WaitSingleMutant)
