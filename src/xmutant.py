#!/usr/bin/env python
# vim: set nospell:
import sys
import json
import inspect
import mutators
from logger import out
import mu
import coverage
import cov
import config
import tests
import argparse

class MutationFailed(Exception): pass

def dumper(obj):
  try: return obj.toJSON()
  except: return obj.__dict__

def testmod(module):
  c = coverage.coverage(source=[module.__name__])
  with cov.Cov(c):
    if not(tests.runAllTests(module)):
      raise MutationFailed("Not all tests passed before mutation")
  __, lines, not_covered, __ = c.analysis(module)

  muscores = {}
  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    checks = getattr(function, 'checks',[])
    skipm = getattr(function, 'skips',[])
    out().info("Mutating %s" % name)
    scores = [m.runTests(module, function, set(not_covered), skipm, checks)
        for m in mutators.allm()]
    s = mu.summarize(scores)
    print name,s
    muscores[name] = s
  return muscores

def main(args):
  try:
    with open('config.json') as c: config.t = json.load(c)
  except: pass
  config.config['MaxTries'] = args.attempts
  module = __import__(args.module)
  try:
    result = dict(config=config.config)
    mu_scores = testmod(module)
    score = mu.summarize(mu_scores.values())
    out().info(score)
    print score
    result['score'] = mu_scores
    with open('logs/score.%s.json' % (module.__name__), 'w') as f:
      f.write(json.dumps(result, indent=2, default=dumper) + "\n")
  except MutationFailed as m: out().error(m)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-a', '--attempts', type=int, help="Number of attempts",
      default=config.MaxTries)
  parser.add_argument("module", help="module to test")
  args = parser.parse_args()
  main(args)

# based on mutant by "Michael Stephens <me@mikej.st>" BSD License
