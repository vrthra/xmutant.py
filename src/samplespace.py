import numpy
import numpy.random
import random

class SampleSpace(object):
  class Unhandled(Exception):
    def __init__(self, str):
      self.e = str

  def weightedIndex(self, size):
    if getattr(self, 'wi', None) == None:
      self.wi = dict()
    if size not in self.wi:
      v = [1.0/i for i in xrange(1,size+1)]
      s = sum(v)
      self.wi[size] = [i/s for i in v]
    return self.wi[size]

  def typeSP(self, maxspace, maxtries, x):
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
  
  # bool int float long complex
  # str, unicode, list, tuple, bytearray, buffer, xrange
  def mySP(self, maxspace, maxtries, x):
    if type(x) == type:
      return self.typeSP(maxspace, maxtries, x)
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
    else:
      raise Unhandled("Unhandled type %s" % str(x))

  def tupleSP(self, space, maxtries, argstruct):
    args = []
    for x in argstruct:
      args.append(self.mySP(space, maxtries, x))
    for _ in range(maxtries):
      yield [next(i) for i in args]

  def listSP(self, space, maxtries, argstruct):
    # xs = [int, [int], (str, int)], i = 1
    # x == [int]
    v = self.pintSP(space, maxtries)
    for i in v:
      arr = list(self.mySP(space, i, argstruct[0]))
      random.shuffle(arr)
      yield arr
    else:
      out().debug("ERROR we dont know how to deal with this yet")

  def strSP(self, space, n):
    v = self.intSP(space, n)
    arr = string.letters + string.digits + ' ' + "\n"
    while True:
      yield "".join(random.choice(arr) for x in xrange(next(v)))

  def boolSP(self, space, n):
    while True:
      r = numpy.random.choice([0,1])
      if r == 0: yield True
      else: yield False

  def pintSP(self, space, n):
    p = self.weightedIndex(space)
    v = numpy.random.choice(xrange(0,space), n, replace=False, p=p)
    v.sort()
    for x in v:
      yield x

  def intSP(self, space, n):
    v = self.pintSP(space, n)
    for x in v:
      r = numpy.random.choice([0,1])
      if x == 0: yield 0
      elif r == 0: yield -x
      else: yield x

  def floatSP(self, space, n):
    v = self.intSP(space, n)
    for x in v:
      r = numpy.random.choice([0,1])
      if x == 0: yield 0
      elif r == 0: yield 1.0/x
      else: yield x

  def __init__(self, maxspace, maxtries):
    self.maxspace = maxspace
    self.maxtries = maxtries

  def genArgs(self, argstruct):
    args = []
    for x in argstruct:
      args.append(self.mySP(self.maxspace, self.maxtries, x))
    for _ in range(self.maxtries):
      yield [next(i) for i in args]

