# vim: set nospell:
# based on mutant by "Michael Stephens <me@mikej.st>" BSD License
# TODO: consider using xdis rather than munge it myself.

import dis
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
        self.opcodes = list(dis.get_instructions(self.func.__code__))
        self.ops = [x.opcode for x in self.opcodes]
        self.args = [x.arg for x in self.opcodes]

    def build(self):
        code = bytes([i if i is not None else 0 for i in sum(zip(self.ops, self.args), ())])
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
