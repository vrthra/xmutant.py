class MuScore(object):
  def __init__(self, nmutants, covering, tdetected, requivalent, rnot_equivalent=0, cskipped=0):
    self.nmutants, self.covering, self.tdetected, self.requivalent, self.rnot_equivalent, self.cskipped = \
        nmutants, covering, tdetected, requivalent, rnot_equivalent, cskipped
    num = nmutants - requivalent
    self.score = -1 if num == 0 else tdetected * 100.0/num
  def __str__(self):
    if self.nmutants == self.requivalent:
      return "Mutants: %d, Covering %d, Detected: %d, Equivalents: %d" % \
        (self.nmutants, self.covering, self.tdetected, self.requivalent)
    return "Mutants: %d, Covering %d, Detected: %d, Equivalents: %d, Score: %f%%" % \
        (self.nmutants, self.covering, self.tdetected, self.requivalent, \
        self.tdetected * 100.0/(self.nmutants - self.requivalent))
  def failed(self):
    return self.nmutants == 0

  def vals(self):
    return vars(self)

  def jdefault(self):
    return self.__dict__


def summarize(muarr):
  nmutants = sum([i.nmutants for i in muarr])
  covering = sum([i.covering for i in muarr])
  tdetected = sum([i.tdetected for i in muarr])
  requivalent = sum([i.requivalent for i in muarr])
  rnot_equivalent = sum([i.rnot_equivalent for i in muarr])
  cskipped = sum([i.cskipped for i in muarr])
  return MuScore(nmutants, covering, tdetected, requivalent, rnot_equivalent, cskipped)

