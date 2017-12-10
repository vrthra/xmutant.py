# vim: set nospell:
# based on mutant by "Michael Stephens <me@mikej.st>" BSD License

import dis
import opobj
import types


class Function(object):
    """
    Make modifying functions a little nicer.
    """

    def __init__(self, func):
        self.func = func
        self.docstring = func.__doc__
        self.consts = list(func.__code__.co_consts[1:])
        self.parse_bytecode()

    def parse_bytecode(self):
        opcodes = [x for x in self.func.__code__.co_code]
        lines = dict(dis.findlinestarts(self.func.__code__))
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
        code = bytes([x.opcode for x in self.opcodes])
        consts = [self.docstring]
        consts.extend(self.consts)
        if type(self.func) == types.FunctionType:
            fc = self.func.__code__
            newfc = type(fc)(fc.co_argcount, fc.co_kwonlyargcount, fc.co_nlocals, fc.co_stacksize,
                             fc.co_flags, code, tuple(consts), fc.co_names,
                             fc.co_varnames, fc.co_filename, fc.co_name,
                             fc.co_firstlineno, fc.co_lnotab, fc.co_freevars,
                             fc.co_cellvars)

            new_func = types.FunctionType(newfc, self.func.__globals__,
                                          name=self.func.__name__,
                                          argdefs=self.func.__defaults__,
                                          closure=self.func.__closure__)
            return new_func
        elif type(self.func) == types.MethodType:
            fc = self.func.im_func.__code__
            newfc = type(fc)(fc.co_argcount, fc.co_kwonlyargcount, fc.co_nlocals, fc.co_stacksize,
                             fc.co_flags, code, tuple(consts), fc.co_names,
                             fc.co_varnames, fc.co_filename, fc.co_name,
                             fc.co_firstlineno, fc.co_lnotab, fc.co_freevars,
                             fc.co_cellvars)
            new_func = types.FunctionType(newfc, self.func.__globals__,
                                          name=self.func.__name__,
                                          argdefs=self.func.__defaults__,
                                          closure=self.func.__closure__)
            new_func = types.MethodType(new_func, None, self.func.im_class)
            return new_func

    def name(self):
        return self.func.__name__
