#!/usr/bin/env python
# vim: set nospell:
import json
import inspect
import mutants
import mu
import coverage
import config
import tests
import argparse
import os

class Cov():
    def __init__(self, cov):
        self.cov = cov

    def __enter__(self):
        self.cov.start()
        return self.cov

    def __exit__(self, type, value, traceback):
        self.cov.stop()

class MutationFailed(Exception): pass


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


def testmod(module):
    c = coverage.coverage(source=[module.__name__])
    with Cov(c):
        if not (tests.runAllTests(module, 'Coverage')):
            raise MutationFailed("Not all tests passed before mutation")
    __, lines, not_covered, __ = c.analysis(module)

    muscores = {}

    for (cname, clz) in inspect.getmembers(module, inspect.isclass):
        checks = getattr(clz, 'checks', [])
        skipm = getattr(clz, 'skips', [])
        skipit = getattr(clz, 'skipit', None)
        if checks == None:
            print("Skipping %s" % cname)
            continue
        for (name, function) in inspect.getmembers(clz, inspect.ismethod):
            checks = getattr(function, 'checks', [])
            skipm = getattr(function, 'skips', [])
            skipit = getattr(function, 'skipit', None)
            if skipit != None:
                print("Skipping %s" % name)
                continue
            scores = [m.runTests(module, clz, function.im_func, set(not_covered), skipm, checks)
                      for m in mutants.allm()]
            s = mu.summarize(scores)
            key = cname + '.' + name
            print(key, s)
            muscores[cname + '.' + name] = s

    for (name, function) in inspect.getmembers(module, inspect.isfunction):
        checks = getattr(function, 'checks', [])
        skipm = getattr(function, 'skips', [])
        skipit = getattr(function, 'skipit', None)
        if skipit != None:
            print("Skipping %s" % name)
            continue
        print("Mutating %s" % name)
        scores = [m.runTests(module, None, function, set(not_covered), skipm, checks)
                  for m in mutants.allm()]
        s = mu.summarize(scores)
        print(name, s)
        muscores[name] = s
    return muscores


def main(args):
    try:
        with open('config.json') as c:
            config.t = json.load(c)
    except:
        pass
    config.config['MaxTries'] = args.attempts
    module = __import__(args.module)
    fresult = 'score/%s/%s.%s.json' % (args.ztag, config.config['MaxTries'], module.__name__)
    try:
        result = dict(config=config.config)
        mu_scores = testmod(module)
        score = mu.summarize(mu_scores.values())
        print(score)
        print(score)
        result['score'] = mu_scores
        result['module'] = args.module
        if not os.path.exists(os.path.dirname(fresult)): os.makedirs(os.path.dirname(fresult))
        umask_original = os.umask(0)
        try:
            with os.fdopen(os.open(fresult, os.O_WRONLY | os.O_CREAT, 0o666), 'w') as f:
                f.write(json.dumps(result, indent=2, default=dumper) + "\n")
        finally:
            os.umask(umask_original)

    except MutationFailed as m:
        print(m, file=sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--attempts', type=int, help="Number of attempts",
                        default=config.MaxTries)
    parser.add_argument('-z', '--ztag', help="tag", default='x')
    parser.add_argument("module", help="module to test")

    args = parser.parse_args()
    main(args)
