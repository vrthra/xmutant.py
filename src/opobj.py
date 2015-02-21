import dis

class Opcode(object):
  """
  Make handling Python bytecode a little nicer.
  """

  def __init__(self, opcode, lineno, arg1=None, arg2=None):
    self.opcode, self.lineno, self.name = opcode,lineno,dis.opname[opcode]
    self.arg1, self.arg2 = arg1, arg2

  def __repr__(self):
    arg = ''
    if self.has_argument(): arg = self.arg()
    return "%s<%d>(%s)" % (self.name, self.lineno, self.arg())

  def __str__(self):
    v = chr(self.opcode)
    if self.has_argument(): v += chr(self.arg1) + chr(self.arg2)
    return v

  def has_argument(self):
    return self.opcode > dis.HAVE_ARGUMENT

  def arg(self):
    return self.arg1 | (self.arg2 << 8)

