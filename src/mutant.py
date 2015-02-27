#!/usr/bin/env python
# vim: set nospell:
import sys
import json
import inspect
import coverage
import mutators
from logger import out
import mu
import config
import tests

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
  failed = tests.runAllTests(module)
  cov.stop()
  if failed: raise MutationFailed()

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
    result = dict()
    result['MaxSpace'] = config.MaxSpace
    result['MaxTries'] = config.MaxTries
    result['Timeout'] = "(%s,%s,%s)" % (config.WaitSingleFn, config.WaitSingleMutant, config.WaitTestRun)
    mu_scores = testmod(module)
    score = mu.summarize(mu_scores.values())
    out().info(score)
    print score

    result['score'] = mu_scores
    with open('score.txt', 'w') as f:
      f.write(json.dumps(result, indent=2, default=dumper))
      f.write("\n")
  except MutationFailed:
      out().error("Error: tests failed without mutation")

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

