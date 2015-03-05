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

  def cmutants(self, c, fn):
    return self.op.cmutants(c,fn)

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
    return mv == ov

  def evalChecks(self, myargnames, checks):
    # default is all int
    if checks == None or checks == []:
      return [int for i in myargnames]
    return [checks[i] for i in myargnames]

  def checkEquivalence(self, module, fname, ofunc, mfunc, checks):
    nvars = ofunc.func_code.co_argcount
    myargnames = ofunc.func_code.co_varnames[0:nvars]
    struct = self.evalChecks(myargnames,checks)
    space = samplespace.SampleSpace(config.config['MaxSpace'], config.config['MaxTries'])
    myargs = space.genArgs(struct)
    for arginst in myargs:
      res = self.checkSingle(module, fname, ofunc, mfunc, arginst)
      if not(res):
        print ">>", fname, arginst
        return False
    return True

  def evalMutant(self, myargs):
    (mutant_func, line, msg, module, claz, function, not_covered, checks) = myargs
    covering = False
    if line not in not_covered:
      covering = True
      if claz:
        setattr(claz, function.func_name, mutant_func)
      else:
        setattr(module, function.func_name, mutant_func)
      passed = tests.runAllTests(module)
      if claz:
        setattr(claz, function.func_name, mutant_func)
      else:
        setattr(module, function.func_name, function)
      if not(passed): return config.FnRes['Detected']
      # potential equivalent!
    prefix = claz.__name__ + '.' if claz else ''
    eq = self.checkEquivalence(module, prefix + function.func_name, function, mutant_func, checks)
    if not(eq): return config.FnRes['NotEq'] # established non-equivalence by random.
    return config.FnRes['ProbEq']

  def runTests(self, module, claz, function, not_covered, skip_ops, checks):
    mutant_count = 0
    detected = 0
    equivalent = 0
    not_equivalent = 0
    skipped = 0
    covered = 0

    tomap = []
    for mutant_func, line, msg in self.mutants(function):
      out().info("op %s" % msg)
      if msg in skip_ops:
        skipped += 1
        continue
      else:
        if line not in not_covered:
          covered += 1
          tomap += [(mutant_func, line, msg, module, claz, function, not_covered, checks)]

    res = mpool.parmap(self.evalMutant, tomap)
    eqv = []
    for (ret,m) in zip(res, tomap):
      if ret == config.FnRes['TimedOut']:
        pass
      elif ret == config.FnRes['Detected']:
        detected += 1
      elif ret == config.FnRes['NotEq']: # detected by random
        not_equivalent +=1
      elif ret == config.FnRes['ProbEq']:
        (_, l, msgs, m, c, f, _, _) = m
        v = "%s:%s.%s %s" % (l, m.__name__, f.func_name, msgs)
        eqv.append(v)

        out().info("pEquivalent %s: %s.%s - [%s]" % (l, m.__name__, f.func_name, msgs))
        equivalent +=1
      else:
        raise Invalid("Invalid output from evalMutant")
      mutant_count += 1
    return mu.MuScore(mutant_count, covered, detected, equivalent, not_equivalent, skipped, eqv)

