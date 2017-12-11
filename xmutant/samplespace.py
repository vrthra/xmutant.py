import itertools
import config
import numpy
import numpy.random
import random
import string
import sys
import time
import typ

StrArr = string.ascii_letters + string.digits + ' ' + '\r\n'


class Unhandled(Exception): pass


class SampleSpace(object):
    def weightedIndex(self, size):
        """
        >>> sp = SampleSpace(100,10)
        >>> sp.weightedIndex(3)
        [0.5454545454545455, 0.27272727272727276, 0.18181818181818182]
        """
        if getattr(self, 'wi', None) == None:
            self.wi = dict()
        if size not in self.wi:
            v = [1.0 / i for i in range(1, size + 1)]
            s = sum(v)
            self.wi[size] = [i / s for i in v]
        return self.wi[size]

    def pintSP(self, maxspace, maxtries):
        """
        >>> numpy.random.seed(0)
        >>> sp = SampleSpace(100,10)
        >>> i = sp.pintSP(100,10)
        >>> [next(i), next(i), next(i)]
        [3, 4, 8]
        >>> numpy.random.seed(10)
        >>> sp = SampleSpace(100,10)
        >>> i = sp.pintSP(100,10)
        >>> [next(i), next(i), next(i)]
        [0, 1, 2]
        >>> [next(i), next(i), next(i)]
        [6, 14, 26]
        """
        p = self.weightedIndex(maxspace)
        arr = numpy.random.choice(range(maxspace), maxtries, replace=False, p=p)
        for x in sorted(arr):
            yield x

    def boolSP(self):
        """
        >>> numpy.random.seed(0)
        >>> sp = SampleSpace(100,10)
        >>> i = sp.boolSP()
        >>> [next(i), next(i), next(i)]
        [True, False, False]
        """
        while True: yield numpy.random.choice([0, 1]) == 0

    def intSP(self):
        """
        >>> numpy.random.seed(0)
        >>> sp = SampleSpace(100,10)
        >>> i = sp.intSP()
        >>> [next(i), next(i), next(i)]
        [3, -4, -8]
        >>> [next(i), next(i), next(i)]
        [9, 12, 15]
        """
        v = self.pintSP(self.maxspace, self.maxtries)
        for x in v:
            r = numpy.random.choice([0, 1])
            if x == 0:
                yield 0
            elif r == 0:
                yield -x
            else:
                yield x

    def longSP(self):
        """
        >>> numpy.random.seed(0)
        >>> sp = SampleSpace(100,10)
        >>> i = sp.longSP()
        >>> [next(i), next(i), next(i)]
        [3, -4, -8]
        >>> [next(i), next(i), next(i)]
        [9, 12, 15]
        """
        return self.intSP()

    def strSP(self):
        """
        >>> numpy.random.seed(0)
        >>> random.seed(0)
        >>> sp = SampleSpace(100,10)
        >>> i = sp.strSP()
        >>> [next(i), next(i), next(i)]
        ['2XB', '', '']
        >>> [next(i), next(i), next(i)]
        ['qHAYtEL7G', 'sXOq7\\r06uV6S', 'EgCN7 F4q0JaUz1']
        """
        v = self.intSP()
        while True: yield ''.join(random.choice(StrArr) for x in range(next(v)))

    def floatSP(self):
        """
        >>> numpy.random.seed(0)
        >>> sp = SampleSpace(100,10)
        >>> i = sp.floatSP()
        >>> [next(i), next(i), next(i)]
        [0.3333333333333333, -4, 8]
        >>> [next(i), next(i), next(i)]
        [0.1111111111111111, 0.08333333333333333, 0.06666666666666667]
        """
        v = self.intSP()
        for x in v:
            r = numpy.random.choice([0, 1])
            if x == 0:
                yield 0
            elif r == 0:
                yield 1.0 / x
            else:
                yield x

    # bool int float long complex
    # str, unicode, list, tuple, bytearray, buffer, range
    def mySP(self, x):
        if type(x) == type:
            if x == bool:
                return self.boolSP()
            elif x == int:
                return self.intSP()
            elif x == long:
                return self.longSP()
            elif x == float:
                return self.floatSP()
            elif x == str:
                return self.strSP()
            else:
                raise Unhandled("Unhandled tuple primary type %s" % str(x))
        elif type(x) == list:
            return self.listSP(x)  # sys.maxsize/ptrsiz
        elif type(x) == tuple:
            return self.tupleSP(x)
        elif type(x) == buffer:
            raise Unhandled("Unhandled buffer %s" % str(x))
        elif type(x) == bytearray:
            raise Unhandled("Unhandled bytearray %s" % str(x))
        elif type(x) == range:
            raise Unhandled("Unhandled range %s" % str(x))
        elif type(x) == dict:
            return self.dictSP(x)
        elif type(x) == set:
            return self.setSP(x)
        else:
            if type(x) == str:
                return self.classSP(x)
            else:
                raise Unhandled("Unhandled type %s" % str(x))

    def classSP(self, argname):
        """
        >>> @typ.typ(y=int,x=int)
        ... class Z(object):
        ...    @typ.typ(self='cls.Z', xx=int, yy=int)
        ...    def __init__(self, xx, yy):
        ...       self.x = xx
        ...       self.y = yy
        ...    def __repr__(self):
        ...       return "Z (%s,%s):%s" % (self.x, self.y, self.sum(1))
        ...    @typ.typ(self='cls.Z', xxx=int)
        ...    def sum(self, xxx):
        ...       return self.x + self.y + xxx
        >>> setattr(sys.modules['samplespace'], 'Z', Z)
        >>> numpy.random.seed(0)
        >>> random.seed(0)
        >>> sp = SampleSpace(1000,10)
        >>> i = sp.classSP('samplespace.Z')
        >>> [next(i) for _ in range(3)]
        [Z (1,-9):-7, Z (6,-12):-5, Z (8,14):23]
        """
        m, c = argname.split('.')
        claz = getattr(sys.modules[m], c)
        keys = claz.checks.keys()
        vals = [claz.checks[i] for i in keys]
        for v in self.tupleSP(tuple(vals)):
            d = dict(zip(keys, v))
            x = type(argname, (claz,), d).__new__(claz)
            x.__dict__ = d
            yield x

    def listiter(self, space):
        for r in range(space):
            for i in itertools.product(range(space), repeat=r):
                yield list(i)

    # http://propersubset.com/2010/04/choosing-random-elements.html
    def random_subset(self, iterator, K):
        result = []
        N = 0
        for item in iterator:
            N += 1
            if len(result) < K:
                result.append(item)
            else:
                s = int(random.random() * N)
                if s < K:
                    result[s] = item
        return result

    def intListSP(self):
        for i in self.random_subset(self.listiter(config.MaxListSpace), self.maxtries):
            yield list(i)

    def listSP(self, argstruct):
        """
        >>> numpy.random.seed(0)
        >>> random.seed(0)
        >>> sp = SampleSpace(1000,20)
        >>> i = sp.listSP([int])
        >>> [next(i) for _ in range(3)]
        [[], [3, 0, -7, -12, -17, -1, 2, 14, -16], [0, -59, -58, 73, 5, 11, -79, -6, 19, -64, 52, 43]]
        """
        # if int, optimize for sorts for now. This needs to be
        # made into a plugin.
        if argstruct[0] == int:
            for i in self.intListSP():
                yield i
        # we assume homogenous lists
        v = self.pintSP(self.maxspace, self.maxtries)
        for i in v:
            it = self.mySP(argstruct[0])
            arr = [next(it) for _ in range(i)]
            random.shuffle(arr)
            yield arr

    def tupleSP(self, argstruct):
        """
        >>> numpy.random.seed(0)
        >>> random.seed(0)
        >>> sp = SampleSpace(1000,10)
        >>> i = sp.tupleSP((int,))
        >>> [next(i) for _ in range(3)]
        [(-9,), (12,), (14,)]
        >>> i = sp.tupleSP((int,int))
        >>> [next(i) for _ in range(3)]
        [(1, 0), (-6, -1), (-8, -3)]
        """

        args = [self.mySP(x) for x in argstruct]
        for _ in range(self.maxtries):
            a = [next(i) for i in args]
            yield tuple(a)

    def setSP(self, argstruct):
        """
        >>> numpy.random.seed(0)
        >>> random.seed(0)
        >>> sp = SampleSpace(1000,14)
        >>> i = sp.setSP({int})
        >>> [next(i) for _ in range(2)]
        [set([0, 193, -30, -189, -57, 11, -17, -67, -1]), set([0, 2, 25, -154, -54, -15, 52, -9, -7, 74, -1, -481])]
        """
        for a in self.listSP(list(argstruct)):
            yield set(a)

    def dictSP(self, argstruct):
        """
        >>> numpy.random.seed(0)
        >>> random.seed(0)
        >>> sp = SampleSpace(1000,14)
        >>> i = sp.dictSP({int:int})
        >>> [next(i) for _ in range(2)]
        [{0: 0, 193: -54, -30: 9, -57: -10, 11: -2, 189: -31, 17: -5, -67: 15, -1: 1}, {0: 0, 2: -7, 3: -14, -60: -38, 8: -20, 74: -96, -126: -408, -17: -24, -75: 363, -296: -542, -261: 535, -1: -2}]
        """
        # we assume homogenous keys and values
        for a in self.listSP([argstruct.items()[0]]):
            yield dict(a)

    def genArgs(self, argstruct):
        return self.tupleSP(argstruct)

    def __init__(self, maxspace, maxtries):
        self.maxspace, self.maxtries = maxspace, maxtries
