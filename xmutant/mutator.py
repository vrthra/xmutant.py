# vim: set nospell:
import sys
import copy
import alarm
import mu
import config
import tests
import warnings


class Invalid(Exception): pass


class Mutator(object):
    def __init__(self, op):
        self.op = op

    def mutants(self, fn):
        return self.op.mutants(fn)

    def identifier(self, line, i, index, module, claz, func):
        prefix = claz.__name__ + '.' if claz else ''
        fname = prefix + func.__name__
        return "%s:%s.%s_%s:%s" % (line, module.__name__, fname, i, index)

    def evalMutant(self, myargs):
        (mutant_func, line, i, index, msg, module, claz, function, not_covered, checks) = myargs
        if line not in not_covered:
            if claz:
                setattr(claz, function.__name__, mutant_func)
                setattr(module, claz.__name__, claz)
            else:
                setattr(module, function.__name__, mutant_func)
            passed = tests.runAllTests(module, msg)
            if claz:
                setattr(claz, function.__name__, mutant_func)
                setattr(module, claz.__name__, claz)
            else:
                setattr(module, function.__name__, function)
            if not (passed): return config.FnDetected
        return config.FnNotDet

    def getEvalArgs(self, module, claz, function, skip_ops, not_covered, checks):
        mutants = list(self.mutants(function))
        tomap = [
            (mutant_func, line, i, index, msg, module, claz, function, not_covered, checks)
            for mutant_func, line, i, index, msg in mutants if msg not in skip_ops]

        skipped = len(mutants) - len(tomap)
        covered = [l for (_, l, _i, _index, _msg, _mod, _claz, _f, _nc, _c) in tomap
                   if l not in not_covered]
        return (tomap, skipped, len(covered))

    def runTests(self, module, claz, function, not_covered, skip_ops, checks):
        if checks == None or checks == []:
            raise Invalid("Invalid type for %s:%s:%s" % (module.__name__, str(claz), function.__name__))

        tomap, skipped, covered = self.getEvalArgs(module, claz, function, skip_ops, not_covered, checks)

        results = [self.evalMutant(m) for m in  tomap]
        eqv = []
        timedout = []
        detected = []
        not_detected = []

        for (ret, mp) in zip(results, tomap):
            (_, l, i, index, msg, m, c, f, _, _) = mp
            myid = self.identifier(l, i, index, m, c, f) + " " + msg
            print("runTest results: %s" % myid)

            if ret == config.FnTimedOut:
                timedout.append(myid)
                print("pEquivalent Timedout %s %s" % (myid, msg))

            elif ret == config.FnDetected:
                detected.append(myid)
                print("Detected %s %s" % (myid, msg))

            elif ret == config.FnNotDet:
                not_detected.append(myid)
                print("NotDetected %s %s" % (myid, msg))

            else:
                raise Invalid("Invalid return code %d" % ret)

        return mu.MuScore(len(results), covered, len(detected), len(not_detected), skipped, eqv, timedout)
