import doctest
import mutants
import inspect
import alarm
import config
import coverage

class MuScore(object):
    def __init__(self, nmutants, covering, tdetected, rnot_detected=0, skipped=0, eqv=[], timedout=[]):
        self.__dict__.update(i for i in locals().items() if i[0] != 'self')
        self.rtimedout = len(timedout)
        num = self.nmutants - self.rtimedout
        self.score = -1 if num == 0 else tdetected * 100.0 / num

    def __str__(self):
        return "Mutants: %d, Covering %d, Detected: %d, Timedout: %d, Score: %f%%" % \
               (self.nmutants, self.covering, self.tdetected, self.rtimedout, \
                self.tdetected * 100.0 / self.nmutants)

    def failed(self):
        return self.nmutants == 0


def summarize(muarr):
    nmutants = sum([i.nmutants for i in muarr])
    covering = sum([i.covering for i in muarr])
    tdetected = sum([i.tdetected for i in muarr])
    rnot_detected = sum([i.rnot_detected for i in muarr])
    skipped = sum([i.skipped for i in muarr])
    eqv = sum([i.eqv for i in muarr], [])
    timedout = sum([i.timedout for i in muarr], [])
    return MuScore(nmutants, covering, tdetected, rnot_detected, skipped, eqv, timedout)

class Cov():
    def __init__(self, cov):
        self.cov = cov

    def __enter__(self):
        self.cov.start()
        return self.cov

    def __exit__(self, type, value, traceback):
        self.cov.stop()

class MutationFailed(Exception): pass

def pr(v): return True

def testmod(module):
    c = coverage.coverage(source=[module.__name__])
    with Cov(c):
        if not (runAllTests(module, 'Coverage')):
            raise MutationFailed("Not all tests passed before mutation")
    __, lines, not_covered, __ = c.analysis(module)

    muscores = {}

    for (cname, clz) in inspect.getmembers(module, inspect.isclass):
        checks = getattr(clz, 'checks', [])
        skipm = getattr(clz, 'skips', [])
        skipit = getattr(clz, 'skipit', None)
        if checks == None:
            print("Skipping %s" % cname)
            continue
        for (name, function) in inspect.getmembers(clz, inspect.ismethod):
            checks = getattr(function, 'checks', [])
            skipm = getattr(function, 'skips', [])
            skipit = getattr(function, 'skipit', None)
            if skipit != None:
                print("Skipping %s" % name)
                continue
            scores = [m.runTests(module, clz, function.im_func, set(not_covered), skipm, checks)
                      for m in mutants.allm()]
            s = summarize(scores)
            key = cname + '.' + name
            print(key, s)
            muscores[cname + '.' + name] = s

    for (name, function) in inspect.getmembers(module, inspect.isfunction):
        checks = getattr(function, 'checks', [])
        skipm = getattr(function, 'skips', [])
        skipit = getattr(function, 'skipit', None)
        if skipit != None:
            print("Skipping %s" % name)
            continue
        print("Mutating %s" % name)
        scores = [m.runTests(module, None, function, set(not_covered), skipm, checks)
                  for m in mutants.allm()]
        s = summarize(scores)
        print(name, s)
        muscores[name] = s
    return muscores

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
