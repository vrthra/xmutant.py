# vim: set nospell:
import sys
import alarm
import os
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
      warnings.filterwarnings('error')
      with alarm.Alarm(config.t['WaitSingleFn']): return fn(*i)
    except alarm.Alarm.Alarm:
      raise
    except:
      (e,v,tb) = sys.exc_info()
      out().debug("caught <%s> : %s - %s" % (e, v, os.getpid()))
      return e

  def checkSingle(self, module, fname, ofunc, mfunc, i):
    mv, ov = None, None
    try:
      out().debug("Test OF >%s %s" % (fname, i))
      ov = self.callfn(ofunc,i)
      out().debug("Test MF >%s %s" % (fname, i))
      mv = self.callfn(mfunc,i)
      out().debug("Test _F <%s %s" % (fname, i))
    except alarm.Alarm.Alarm:
      out().debug("Test TF #%s %s" % (fname, i))
      # if we got a timeout on ov, then both ov and mv are None
      # so we return True because we cant decide if original function
      # times out. However, if mv times out, mv == None, and ov != None
      # so we detect. Unfortunately, we assume ov != None for valid
      # functions which may not be true!
      pass
    return (mv, ov)

  def evalChecks(self, myargnames, checks):
    return [checks[i] for i in myargnames]

  def checkEquivalence(self, msg, module, line, fname, ofunc, mfunc, checks):
    nvars = ofunc.func_code.co_argcount
    myargnames = ofunc.func_code.co_varnames[0:nvars]
    struct = self.evalChecks(myargnames,checks)
    space = samplespace.SampleSpace(config.config['MaxSpace'], config.config['MaxTries'])
    myargs = space.genArgs(struct)
    for arginst in myargs:
      (mv, ov) = self.checkSingle(module, fname, ofunc, mfunc, arginst)
      if mv != ov:
        out().info("<NonEq Detected - [ %s ] > %s:%s(%s) (%s <> %s)" % (msg, line, fname, arginst, mv, ov))
        return False
    return True

  def evalMutant(self, myargs):
    (mutant_func, line, msg, module, claz, function, not_covered, checks) = myargs
    if line not in not_covered:
      if claz:
        setattr(claz, function.func_name, mutant_func)
        setattr(module, claz.__name__, claz)
      else:
        setattr(module, function.func_name, mutant_func)
      passed = tests.runAllTests(module, msg)
      if claz:
        setattr(claz, function.func_name, mutant_func)
        setattr(module, claz.__name__, claz)
      else:
        setattr(module, function.func_name, function)
      if not(passed): return config.FnDetected
      # potential equivalent!
    prefix = claz.__name__ + '.' if claz else ''
    eq = self.checkEquivalence(msg, module, line, prefix + function.func_name, function, mutant_func, checks)
    if not(eq): return config.FnNotEq # established non-equivalence by random.
    return config.FnProbEq

  def getEvalArgs(self, module, claz, function, skip_ops, not_covered, checks):
    mutants = list(self.mutants(function))
    tomap = [
        (mutant_func, line, msg, module, claz, function, not_covered, checks)
        for mutant_func, line, msg in mutants if msg not in skip_ops]

    skipped = len(mutants) - len(tomap)
    covered = [l for (_, l, _msg, _mod, _claz, _f, _nc, _c) in tomap
        if l not in not_covered]
    return (tomap, skipped, len(covered))

  def runTests(self, module, claz, function, not_covered, skip_ops, checks):
    if checks == None or checks == []:
      raise Invalid("Invalid type for %s:%s:%s" % (module.__name__, str(claz), function.func_name))

    tomap, skipped, covered = self.getEvalArgs(module, claz, function, skip_ops, not_covered, checks)

    res = mpool.parmap(self.evalMutant, tomap)
    eqv = []
    timedout = []
    detected = [ret for ret in res if ret == config.FnDetected]
    not_equivalent = [ret for ret in res if ret == config.FnNotEq] # detected by random

    for (ret,mp) in zip(res, tomap):
      (_, l, msg, m, c, f, _, _) = mp
      v = "%s:%s.%s %s" % (l, m.__name__, f.func_name, msg)
      out().info("%s: op %s" % (l, msg))

      if ret == config.FnTimedOut:
        timedout.append(v)
        out().info("pEquivalent Timedout %s: %s.%s - [%s]" % (l, m.__name__, f.func_name, msg))
      elif ret == config.FnProbEq:
        eqv.append(v)
        out().info("pEquivalent %s: %s.%s - [%s]" % (l, m.__name__, f.func_name, msg))

    return mu.MuScore(len(res), covered, len(detected), len(not_equivalent), skipped, eqv, timedout)

