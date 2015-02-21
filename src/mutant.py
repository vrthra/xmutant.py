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
  fails = mutators.runAllTests(module)[0]
  if fails > 0: return (0, 0)

  mutations = [
      mutators.ComparisonMutation(),
      mutators.ModifyConstantMutation(),
      mutators.JumpMutation()]

  fails = 0
  attempts = 0

  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    print "Testing %s" % name
    for mutation in mutations:
      f, a = mutation.runTests(module, function)

      fails += f
      attempts += a
    print

  return fails, attempts

if __name__ == '__main__':
  module = __import__(sys.argv[1])
  (fails, attempts) = testmod(module)
  if attempts == 0:
    print "Error: tests failed without mutation"
  else:
    print "Mutants: %d, Not Detected: %d, Score: %f%%" % (attempts, fails, 100.0 - fails * 100.0 / attempts)

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

