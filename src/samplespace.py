import numpy
import numpy.random
import random
import string
import sys

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

  def strSP(self):
    v = self.intSP()
    while True: yield ''.join(random.choice(StrArr) for x in xrange(next(v)))

  def boolSP(self):
    while True: yield numpy.random.choice([0,1]) == 0

  def pintSP(self, maxspace, maxtries):
    p = self.weightedIndex(maxspace)
    arr = numpy.random.choice(xrange(maxspace), maxtries, replace=False, p=p)
    for x in sorted(arr):
      yield x

  def longSP(self):
    return self.intSP()

  def intSP(self):
    v = self.pintSP(self.maxspace, self.maxtries)
    for x in v:
      r = numpy.random.choice([0,1])
      if x == 0: yield 0
      elif r == 0: yield -x
      else: yield x

  def floatSP(self):
    v = self.intSP()
    for x in v:
      r = numpy.random.choice([0,1])
      if x == 0: yield 0
      elif r == 0: yield 1.0/x
      else: yield x

  # bool int float long complex
  # str, unicode, list, tuple, bytearray, buffer, xrange
  def mySP(self,x):
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
      return self.listSP(x) # sys.maxsize/ptrsiz
    elif type(x) == tuple:
      return self.tupleSP(x)
    elif type(x) == buffer:
      raise Unhandled("Unhandled buffer %s" % str(x))
    elif type(x) == bytearray:
      raise Unhandled("Unhandled bytearray %s" % str(x))
    elif type(x) == xrange:
      raise Unhandled("Unhandled xrange %s" % str(x))
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
    m,c = argname.split('.')
    claz = getattr(sys.modules[m], c)
    for a in self.dictSP(claz.checks):
      x = type(argname, (claz,), a)()
      yield x


  def listSP(self, argstruct):
    # we assume homogenous lists
    v = self.pintSP(self.maxspace, self.maxtries)
    for i in v:
      it  = self.mySP(argstruct[0])
      arr = [next(it) for _ in range(i)]
      random.shuffle(arr)
      yield arr

  def tupleSP(self, argstruct):
    args = [self.mySP(x) for x in argstruct]
    for _ in range(self.maxtries):
      a = [next(i) for i in args]
      yield a

  def setSP(self, argstruct):
    for a in self.listSP(list(argstruct)):
      yield set(a)

  def dictSP(self, argstruct):
    # we assume homogenous keys and values
    for a in self.listSP([argstruct.items()[0]]):
      yield dict(a)

  def genArgs(self, argstruct):
    return self.tupleSP(argstruct)

  def __init__(self, maxspace, maxtries):
    self.maxspace, self.maxtries = maxspace, maxtries

