#!/usr/bin/env python
# vim: set nospell:
import json
import config
import tests
import argparse
import os

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

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
        mu_scores = tests.testmod(module)
        score = tests.summarize(mu_scores.values())
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

    except tests.MutationFailed as m:
        print(m, file=sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--attempts', type=int, help="Number of attempts",
                        default=config.MaxTries)
    parser.add_argument('-z', '--ztag', help="tag", default='x')
    parser.add_argument("module", help="module to test")

    args = parser.parse_args()
    main(args)
