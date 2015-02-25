#!/usr/bin/env python
# vim: set nospell:
import sys
import random
import inspect
import doctest
import coverage
import mutators
import alarm
import logger
from logger import out

fn_args = {}
g_skip_ops = {}
WaitSingleFn = 10

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

def update_fnargs(module):
  global fn_args
  global g_skip_ops
  finder = doctest.DocTestFinder(exclude_empty=False)
  for test in finder.find(module, module.__name__):
    myargs = ''.join([e.source for e in test.examples if e.source.startswith('args = ')])
    myskips = ''.join([e.source for e in test.examples if e.source.startswith('skips = ')])
    name = test.name[len(module.__name__)+1:]
    if myargs.strip() != '':
      loc, glob = {}, {}
      args = eval(myargs[7:], glob, loc)
      mymax = args[0]['max']
      mymin = args[0]['min']
      fn_args[name] = args
    if myskips.strip() != '':
      loc, glob = {}, {}
      g_skip_ops[name] = eval(myskips[7:], glob, loc)

def testmod(module):
  """
  Mutation test all of a module's functions.
  """
  cov = coverage.coverage(source=[module.__name__])
  cov.start()
  fails = runAllTests(module)
  cov.stop()
  if fails > 0: return (0, 0, 0)

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

  update_fnargs(module)

  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    out().info("Mutating %s" % name)
    for mutator in mymutators:
      nmu, det, f_not_eq, eq, skipped, c = mutator.runTests(module, function, not_covered, (g_skip_ops.get(name) or []))

      mu_count += nmu
      detected += det
      fails += f_not_eq
      equivalent += eq
      skips += skipped
      covered += c
    print

  return (mu_count, detected, equivalent, covered)

if __name__ == '__main__':
  module = __import__(sys.argv[1])
  (mu_count, detected, equivalent, covered) = testmod(module)
  #print fn_args
  if mu_count == 0:
    out().info("Error: tests failed without mutation")
  else:
    out().info("Mutants: %d, Covering %d, Detected: %d, Equivalents: %d, Score: %f%%" % (mu_count, covered, detected, equivalent,  detected * 100.0/ (mu_count - equivalent)))

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

