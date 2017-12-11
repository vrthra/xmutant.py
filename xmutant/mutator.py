# vim: set nospell:
import sys
import copy
import alarm
import mu
import samplespace
import mpool
import config
import tests
from logger import out
import warnings


class Invalid(Exception): pass


class Mutator(object):
    def __init__(self, op):
        self.op = op

    def mutants(self, fn):
        return self.op.mutants(fn)

    def callfn(self, fn, i):
        try:
            ix = copy.deepcopy(i)
            warnings.filterwarnings('error')
            with alarm.Alarm(config.t['WaitSingleFn']):
                return fn(*ix)
        except alarm.Alarm.Alarm:
            raise
        except:
            (e, v, tb) = sys.exc_info()
            out().debug("caught <%s> : %s" % (e, v))
            return e

    def checkSingle(self, module, fname, ofunc, mfunc, i):
        mv, ov = None, None
        try:
            ov = self.callfn(ofunc, i)
            mv = self.callfn(mfunc, i)
        except alarm.Alarm.Alarm:
            out().debug("TF #%s %s" % (fname, i))
            # if we got a timeout on ov, then both ov and mv are None
            # so we return True because we cant decide if original function
            # times out. However, if mv times out, mv == None, and ov != None
            # so we detect. Unfortunately, we assume ov != None for valid
            # functions which may not be true!
            pass
        return (mv, ov)

    def evalChecks(self, myargnames, checks):
        return [checks[i] for i in myargnames]

    def identifier(self, line, i, index, module, claz, func):
        prefix = claz.__name__ + '.' if claz else ''
        fname = prefix + func.__name__
        return "%s:%s.%s_%s:%s" % (line, module.__name__, fname, i, index)

    def checkEquivalence(self, msg, module, line, i, index, claz, ofunc, mfunc, checks):
        prefix = claz.__name__ + '.' if claz else ''
        fname = prefix + ofunc.__name__

        nvars = ofunc.__code__.co_argcount
        myargnames = ofunc.__code__.co_varnames[0:nvars]
        struct = self.evalChecks(myargnames, checks)
        space = samplespace.SampleSpace(config.config['MaxSpace'], config.config['MaxTries'])
        myargs = space.genArgs(struct)
        myid = self.identifier(line, i, index, module, claz, ofunc)
        for arginst in myargs:
            out().debug("Test for mutant %s %s %s" % (myid, msg, arginst))
            (mv, ov) = self.checkSingle(module, fname, ofunc, mfunc, arginst)
            out().debug("Result for original %s %s %s" % (myid, msg, ov))
            out().debug("Result for mutant %s %s %s" % (myid, msg, mv))
            out().debug("V %s %s %s" % (myid, msg, mv == ov))
            if mv != ov:
                out().info("NonEq Detected - [ %s %s ] > (%s) (%s <> %s)" % (myid, msg, arginst, mv, ov))
                return False
        return True

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
            # potential equivalent!
        eq = self.checkEquivalence(msg, module, line, i, index, claz, function, mutant_func, checks)
        if not (eq): return config.FnNotEq  # established non-equivalence by random.
        return config.FnProbEq

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

        results = mpool.parmap(self.evalMutant, tomap)
        eqv = []
        timedout = []
        detected = []
        not_equivalent = []

        for (ret, mp) in zip(results, tomap):
            (_, l, i, index, msg, m, c, f, _, _) = mp
            myid = self.identifier(l, i, index, m, c, f) + " " + msg
            out().info("runTest results: %s" % myid)

            if ret == config.FnTimedOut:
                timedout.append(myid)
                out().info("pEquivalent Timedout %s %s" % (myid, msg))
            elif ret == config.FnProbEq:
                eqv.append(myid)
                out().info("pEquivalent %s %s" % (myid, msg))

            elif ret == config.FnDetected:
                detected.append(myid)
                out().info("Detected %s %s" % (myid, msg))

            elif ret == config.FnNotEq:
                not_equivalent.append(myid)
                out().info("NotEquivalent %s %s" % (myid, msg))

            else:
                raise Invalid("Invalid return code %d" % ret)

        return mu.MuScore(len(results), covered, len(detected), len(not_equivalent), skipped, eqv, timedout)
