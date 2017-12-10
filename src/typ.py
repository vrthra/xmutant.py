# vim: set nospell :

def typ(**checks):
    def annotate(fn, checks=checks):
        fn.checks = checks
        return fn

    return annotate


def skips(**skips):
    def annotate(fn, skips=skips):
        fn.skips = skips
        return fn

    return annotate


def skipit(**skipit):
    def annotate(fn, skipit=True):
        fn.skipit = skipit
        return fn

    return annotate
