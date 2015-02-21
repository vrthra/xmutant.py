#!/usr/bin/env python
# vim: set nospell:
import sys
import random
import inspect
import doctest
import coverage
import mutators

def testmod(module):
  """
  Mutation test all of a module's functions.
  """
  cov = coverage.coverage(source=[module.__name__])
  cov.start()
  fails = mutators.runAllTests(module, first=True)
  cov.stop()
  if fails > 0: return (0, 0)

  __, lines, nc, fmt = cov.analysis(module)
  not_covered = set(nc)

  mymutators = [
      mutators.ComparisonMutation(),
      mutators.ModifyConstantMutation(),
      mutators.JumpMutation()]

  fails = 0
  skips = 0
  attempts = 0

  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    print "Mutating %s" % name
    for mutator in mymutators:
      f, s, a = mutator.runTests(module, function, not_covered)

      fails += f
      skips += s
      attempts += a
    print

  return fails, skips, attempts

if __name__ == '__main__':
  module = __import__(sys.argv[1])
  (fails, skips, attempts) = testmod(module)
  if attempts == 0:
    print "Error: tests failed without mutation"
  else:
    print "Mutants: %d, Not Detected: %d, Skipped: %d, Score: %f%%" % (attempts, fails, skips, 100.0 - (fails + skips) * 100.0 / attempts)

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

