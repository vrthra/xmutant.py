#!/usr/bin/env python
# vim: set nospell:
import json
import inspect
import mutants
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
    if not(tests.runAllTests(module, 'Coverage')):
      raise MutationFailed("Not all tests passed before mutation")
  __, lines, not_covered, __ = c.analysis(module)

  muscores = {}

  for (cname, clz) in inspect.getmembers(module, inspect.isclass):
    checks = getattr(clz, 'checks',[])
    skipm = getattr(clz, 'skips',[])
    skipit = getattr(clz, 'skipit',None)
    if skipit != None:
      out().info("Skipping %s" % cname)
      continue
    for (name, function) in inspect.getmembers(clz, inspect.ismethod):
      checks = getattr(function, 'checks',[])
      skipm = getattr(function, 'skips',[])
      skipit = getattr(function, 'skipit',None)
      if skipit != None:
        out().info("Skipping %s" % name)
        continue
      scores = [m.runTests(module, clz, function, set(not_covered), skipm, checks)
          for m in mutants.allm()]
      s = mu.summarize(scores)
      key = cname + '.' + name
      print key,s
      muscores[cname + '.' + name] = s

  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    checks = getattr(function, 'checks',[])
    skipm = getattr(function, 'skips',[])
    skipit = getattr(function, 'skipit',None)
    if skipit != None:
      out().info("Skipping %s" % name)
      continue
    out().info("Mutating %s" % name)
    scores = [m.runTests(module, None, function, set(not_covered), skipm, checks)
        for m in mutants.allm()]
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
    with open('logs/score.%s.%s.json' % (config.config['MaxTries'], module.__name__), 'w') as f:
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

