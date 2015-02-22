#!/usr/bin/env python
# vim: set nospell:
import sys
import random
import inspect
import doctest
import coverage
import mutators

fn_args = {}

def update_fnargs(module):
  global fn_args
  finder = doctest.DocTestFinder(exclude_empty=False)
  for test in finder.find(module, module.__name__):
    myargs = ''.join([e.source for e in test.examples if e.source.startswith('args = ')])
    if myargs.strip() != '':
      loc, glob = {}, {}
      args = eval(myargs[7:], glob, loc)
      mymax = args[0]['max']
      mymin = args[0]['min']
      fn_args[test.name] = args

def testmod(module):
  """
  Mutation test all of a module's functions.
  """
  cov = coverage.coverage(source=[module.__name__])
  cov.start()
  fails = mutators.runAllTests(module, first=True)
  cov.stop()
  if fails > 0: return (0, 0, 0)

  __, lines, nc, fmt = cov.analysis(module)
  not_covered = set(nc)

  mymutators = [
      mutators.ComparisonMutation(),
      mutators.ModifyConstantMutation(),
      mutators.JumpMutation()]

  fails = 0
  skips = 0
  attempts = 0

  update_fnargs(module)

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
  #print fn_args
  if attempts == 0:
    print "Error: tests failed without mutation"
  else:
    print "Mutants: %d, Not Detected: %d, Skipped: %d, Score: %f%%" % (attempts, fails, skips, 100.0 - (fails + skips) * 100.0 / attempts)

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

