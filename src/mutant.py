#!/usr/bin/env python
# vim: set nospell:
import sys
import json
import random
import inspect
import doctest
import coverage
import mutators
import alarm
import logger
import typ
from logger import out
import mu

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

def dumper(obj):
  try: return obj.toJSON()
  except: return obj.__dict__

class MutationFailed(Exception): pass

def testmod(module):
  """
  Mutation test all of a module's functions.
  """
  cov = coverage.coverage(source=[module.__name__])
  cov.start()
  fails = runAllTests(module)
  cov.stop()
  if fails > 0: raise MutationFailed()

  __, lines, nc, fmt = cov.analysis(module)
  not_covered = set(nc)

  fails = 0
  detected = 0
  equivalent = 0
  skips = 0
  mu_count = 0
  covered = 0

  muscores = {}
  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    checks = getattr(function, 'checks',[])
    skipm = getattr(function, 'skips',[])
    out().info("Mutating %s" % name)
    scores = []
    for mutator in mutators.allm():
      m = mutator.runTests(module, function, not_covered, skipm, checks)
      scores.append(m)
    s = mu.summarize(scores)
    print name,s
    muscores[name] = s
  return muscores

if __name__ == '__main__':
  module = __import__(sys.argv[1])
  try:
    mu_scores = testmod(module)
    score = mu.summarize(mu_scores.values())
    out().info(score)
    print score
    with open('score.txt', 'w') as f:
      f.write(json.dumps(mu_scores, indent=2, default=dumper))
      f.write("\n")
  except MutationFailed:
      out().error("Error: tests failed without mutation")

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

