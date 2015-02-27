import numpy
import numpy.random
import random
import string

StrArr = string.letters + string.digits + ' ' + "\r\n"
class Unhandled(Exception): pass

class SampleSpace(object):

  def weightedIndex(self, size):
    if getattr(self, 'wi', None) == None:
      self.wi = dict()
    if size not in self.wi:
      v = [1.0/i for i in xrange(1,size+1)]
      s = sum(v)
      self.wi[size] = [i/s for i in v]
    return self.wi[size]

  def strSP(self, maxspace, maxtries):
    v = self.intSP(maxspace, maxtries)
    while True: yield ''.join(random.choice(StrArr) for x in xrange(next(v)))

  def boolSP(self, maxspace, maxtries):
    while True: yield numpy.random.choice([0,1]) == 0

  def pintSP(self, maxspace, maxtries):
    p = self.weightedIndex(maxspace)
    arr = numpy.random.choice(xrange(maxspace), maxtries, replace=False, p=p)
    for x in sorted(arr):
      yield x

  def intSP(self, maxspace, maxtries):
    v = self.pintSP(maxspace, maxtries)
    for x in v:
      r = numpy.random.choice([0,1])
      if x == 0: yield 0
      elif r == 0: yield -x
      else: yield x

  def floatSP(self, maxspace, maxtries):
    v = self.intSP(maxspace, maxtries)
    for x in v:
      r = numpy.random.choice([0,1])
      if x == 0: yield 0
      elif r == 0: yield 1.0/x
      else: yield x

  # bool int float long complex
  # str, unicode, list, tuple, bytearray, buffer, xrange
  def mySP(self, maxspace, maxtries, x):
    if type(x) == type:
      if x == bool:
        return self.boolSP(2, maxtries)
      elif x == int:
        return self.intSP(maxspace, maxtries)
      elif x == long:
        return self.intSP(maxspace, maxtries)
      elif x == float:
        return self.floatSP(maxspace, maxtries)
      elif x == str:
        return self.strSP(maxspace, maxtries)
      else:
        raise Unhandled("Unhandled tuple primary type %s" % str(x))
    elif type(x) == list:
      return self.listSP(maxspace/8, maxtries, x) # sys.maxsize/ptrsiz
    elif type(x) == tuple:
      return self.tupleSP(maxspace, maxtries, x)
    elif type(x) == buffer:
      raise Unhandled("Unhandled buffer %s" % str(x))
    elif type(x) == bytearray:
      raise Unhandled("Unhandled bytearray %s" % str(x))
    elif type(x) == xrange:
      raise Unhandled("Unhandled xrange %s" % str(x))
    elif type(x) == dict:
      return self.dictSP(maxspace, maxtries, x)
    elif type(x) == set:
      return self.setSP(maxspace, maxtries, x)
    else:
      raise Unhandled("Unhandled type %s" % str(x))

  def listSP(self, maxspace, maxtries, argstruct):
    # we assume homogenous lists
    v = self.pintSP(maxspace, maxtries)
    for i in v:
      arr = list(self.mySP(maxspace, i, argstruct[0]))
      random.shuffle(arr)
      yield arr

  def tupleSP(self, maxspace, maxtries, argstruct):
    args = [self.mySP(maxspace, maxtries, x) for x in argstruct]
    for _ in range(maxtries):
      yield [next(i) for i in args]

  def setSP(self, maxspace, maxtries, argstruct):
    for a in self.listSP(maxspace, maxtries, list(argstruct)):
      yield set(a)

  def dictSP(self, maxspace, maxtries, argstruct):
    # we assume homogenous keys and values
    for a in self.listSP(maxspace, maxtries, argstruct.items()):
      yield dict(a)

  def genArgs(self, argstruct):
    return self.tupleSP(self.maxspace, self.maxtries, argstruct)

  def __init__(self, maxspace, maxtries):
    self.maxspace, self.maxtries = maxspace, maxtries

