#!/usr/bin/env python
# vim: set nospell:
import json
import sys
import random
import inspect
import doctest
import coverage
import mutators
import alarm
import logger
import typ
from logger import out

g_skip_ops = {}
WaitSingleFn = 10

class MuScore(object):
  def __init__(self, nmutants, covering, detected, equivalent):
    self.nmutants, self.covering, self.detected, self.equivalent = nmutants, covering, detected, equivalent
  def __str__(self):
    if self.nmutants == self.equivalent:
      return "Mutants: %d, Covering %d, Detected: %d, Equivalents: %d" % \
        (self.nmutants, self.covering, self.detected, self.equivalent)
    return "Mutants: %d, Covering %d, Detected: %d, Equivalents: %d, Score: %f%%" % \
        (self.nmutants, self.covering, self.detected, self.equivalent, \
        self.detected * 100.0/(self.nmutants - self.equivalent))
  def failed(self):
    return self.nmutants == 0
  def json(self):
    return json.dumps(vars(self),sort_keys=True, indent=4)

def runAllTests(module):
  finder = doctest.DocTestFinder(exclude_empty=False)
  runner = doctest.DocTestRunner(verbose=False)
  for test in finder.find(module, module.__name__):
    try:
      out().debug("Coverage Test %s" % test.name)
      with alarm.Alarm(WaitSingleFn):
        runner.run(test, out=lambda x: True)
    except alarm.Alarm.Alarm: return 1 # timeout!
    if runner.failures > 0: return runner.failures
  return runner.failures

def testmod(module):
  """
  Mutation test all of a module's functions.
  """
  cov = coverage.coverage(source=[module.__name__])
  cov.start()
  fails = runAllTests(module)
  cov.stop()
  if fails > 0: return MuScore(0, 0, 0, 0)

  __, lines, nc, fmt = cov.analysis(module)
  not_covered = set(nc)

  mymutators = [
      mutators.BoolComparisonMutation(),
      mutators.SetComparisonMutation(),
      mutators.ModifyConstantMutation(),
      mutators.JumpMutation(),
      mutators.UnaryMutation(),
      mutators.BinaryMutation()]

  fails = 0
  detected = 0
  equivalent = 0
  skips = 0
  mu_count = 0
  covered = 0

  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    checks = getattr(function, 'checks',[])
    skipm = getattr(function, 'skips',[])
    out().info("Mutating %s" % name)
    for mutator in mymutators:
      nmu, det, f_not_eq, eq, skipped, c = mutator.runTests(module, function, not_covered, skipm, checks)

      mu_count += nmu
      detected += det
      fails += f_not_eq
      equivalent += eq
      skips += skipped
      covered += c

  return MuScore(mu_count, covered, detected, equivalent)

if __name__ == '__main__':
  module = __import__(sys.argv[1])
  mu_score = testmod(module)
  if mu_score.failed():
    out().info("Error: tests failed without mutation")
    print "Error: tests failed without mutation"
  else:
    out().info(mu_score)
    print mu_score.json()

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

