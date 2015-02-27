# Make sure that WaitSingleMutant is a sane value. the WaitSingleFn is overly
# optimistic and fails to handle cases where we have exception handlers that
# are overly aggressive with 'except:' -- the sigalarm we use gets stuck in
# these exception handlers.
WaitSingleFn = 5
WaitTestRun = 10 * WaitSingleFn
WaitSingleMutant = 100 * WaitSingleFn
MaxTries = 10000
MaxSpace = 1000000
FnRes = dict(TimedOut=0,Detected=1, NotEq=2,ProbEq=3)

