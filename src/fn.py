# vim: set nospell:

import dis
import opobj

class Function(object):
  """
  Make modifying functions a little nicer.
  """

  def __init__(self, func):
    self.func = func
    self.docstring = func.func_code.co_consts[0]
    self.consts = list(func.func_code.co_consts[1:])
    self.parse_bytecode()

  def parse_bytecode(self):
    opcodes = [ord(x) for x in self.func.func_code.co_code]
    lines = dict(dis.findlinestarts(self.func.func_code))
    self.opcodes = []
    i = 0
    while i < len(opcodes):
      if i in lines: lineno = lines[i]
      opcode = opobj.Opcode(opcodes[i], lineno)
      if opcode.has_argument():
        opcode.arg1, opcode.arg2 = opcodes[i + 1], opcodes[i + 2]
        i += 2
      self.opcodes.append(opcode)
      i += 1

  def build(self):
    code = ''.join([str(x) for x in self.opcodes])
    consts = [self.docstring]
    consts.extend(self.consts)
    fc = self.func.func_code
    newfc = type(fc)(fc.co_argcount, fc.co_nlocals, fc.co_stacksize,
             fc.co_flags, code, tuple(consts), fc.co_names,
             fc.co_varnames, fc.co_filename, fc.co_name,
             fc.co_firstlineno, fc.co_lnotab, fc.co_freevars,
             fc.co_cellvars)
    new_func = type(self.func)(newfc, self.func.func_globals,
                   self.func.func_name,
                   self.func.func_defaults,
                   self.func.func_closure)
    return new_func

  def name(self):
    return self.func.func_name
