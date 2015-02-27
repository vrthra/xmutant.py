# vim: set nospell:
import dis
import doctest
import opobj
import fn
import sys
import alarm
import logger
import os
import mu
import samplespace
import util
import config
import tests
from logger import out

class Invalid(Exception): pass

class MutationOp(object):
  def __init__(self):
    pass

  def callfn(self, fn, i):
    try:
      with alarm.Alarm(config.t['WaitSingleFn']): return fn(*i)
    except alarm.Alarm.Alarm:
      raise
    except:
      (e,v,tb) = sys.exc_info()
      out().debug("caught <%s> : %s - %s" % (e, v, os.getpid()))
      return e

  def checkSingle(self, module, fname, ofunc, mfunc, i):
    mv = None
    ov = None
    try:
      out().debug("Test OF >%s %s" % (fname, i))
      ov = self.callfn(ofunc,i)
      out().debug("Test MF >%s %s" % (fname, i))
      mv = self.callfn(mfunc,i)
      out().debug("Test _F <%s %s" % (fname, i))
    except alarm.Alarm.Alarm:
      out().debug("Test TF #%s %s" % (fname, i))
      # if we got a timeout on ov, then both ov and mv are None
      # so we return True because we cant decide if original function
      # times out. However, if mv times out, mv == None, and ov != None
      # so we detect. Unfortunately, we assume ov != None for valid
      # functions which may not be true!
      pass
    return mv == ov

  def evalChecks(self, myargnames, checks):
    if checks == None:
      # default is all int
      return [int for i in myargnames]
    return [checks[i] for i in myargnames]

  def checkEquivalence(self, module, fname, ofunc, mfunc, checks):
    nvars = ofunc.func_code.co_argcount
    myargnames = ofunc.func_code.co_varnames[0:nvars]
    struct = self.evalChecks(myargnames,checks)
    space = samplespace.SampleSpace(config.config['MaxSpace'], config.config['MaxTries'])
    myargs = space.genArgs(struct)
    for arginst in myargs:
      res = self.checkSingle(module, fname, ofunc, mfunc, arginst)
      if not(res): return False
    return True

  def evalMutant(self, myargs):
    (mutant_func, line, msg, module, function, not_covered, checks) = myargs
    covering = False
    if line not in not_covered:
      covering = True
      setattr(module, function.func_name, mutant_func)
      passed = tests.runAllTests(module)
      setattr(module, function.func_name, function)
      if not(passed): return config.FnRes['Detected']
      # potential equivalent!
    eq = self.checkEquivalence(module, function.func_name, function, mutant_func, checks)
    if not(eq): return config.FnRes['NotEq'] # established non-equivalence by random.
    return config.FnRes['ProbEq']

  def runTests(self, module, function, not_covered, skip_ops, checks):
    mutant_count = 0
    detected = 0
    equivalent = 0
    not_equivalent = 0
    skipped = 0
    covered = 0

    tomap = []
    for mutant_func, line, msg in self.mutants(function):
      out().info("op %s" % msg)
      if msg in skip_ops:
        skipped += 1
        continue
      else:
        if line not in not_covered:
          covered += 1
        tomap += [(mutant_func, line, msg, module, function, not_covered, checks)]

    res = util.parmap(self.evalMutant, tomap)
    for (ret,m) in zip(res, tomap):
      if ret == config.FnRes['TimedOut']:
        pass
      elif ret == config.FnRes['Detected']:
        detected += 1
      elif ret == config.FnRes['NotEq']: # detected by random
        not_equivalent +=1
      elif ret == config.FnRes['ProbEq']:
        (_, l, msgs, m, f, _, _) = m
        out().info("pEquivalent %s: %s.%s - [%s]" % (l, m.__name__, f.func_name, msgs))
        equivalent +=1
      else:
        raise Invalid("Invalid output from evalMutant")
      mutant_count += 1
    return mu.MuScore(mutant_count, covered, detected, equivalent, not_equivalent, skipped)

  def mutants(self, function):
    """
    MutationOps should override this to return an iterator of
    mutated functions.
    """
    raise NotImplementedError()


class SetComparisonMutation(MutationOp):
  """
  Swap comparsion operators (e.g. change 'in' to 'not in')
  """
  # ('<', '<=', '==', '!=', '>', '>=', 'in', 'not in', 'is', 'is not', 'exception match', 'BAD')

  def mutants(self, function):
    func = fn.Function(function)
    myops = ['in', 'not in']

    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]

      if opcode.name == 'COMPARE_OP':
        cmp_op = dis.cmp_op[opcode.arg()]
        if cmp_op in myops:
          for op in myops:
            if cmp_op != op:
              n = dis.cmp_op.index(op)
              new_oc = opobj.Opcode(opcode.opcode, opcode.lineno, n >> 8, n & 255)
              func.opcodes[i] = new_oc
              yield (func.build(), opcode.lineno, "scm, %s : swap %s" % (cmp_op, op))
      func.opcodes[i] = opcode
      i += 1

class BoolComparisonMutation(MutationOp):
  """
  Swap comparsion operators (e.g. change '>' to '>=' or '==')
  """
  def mutants(self, function):
    func = fn.Function(function)
    myops = ['<', '<=', '==', '!=', '>', '>=']

    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]

      if opcode.name == 'COMPARE_OP':
        cmp_op = dis.cmp_op[opcode.arg()]
        if cmp_op in myops:
          for op in myops:
            if cmp_op != op:
              n = dis.cmp_op.index(op)
              new_oc = opobj.Opcode(opcode.opcode, opcode.lineno, n >> 8, n & 255)
              func.opcodes[i] = new_oc
              yield (func.build(), opcode.lineno, "bcm, %s : swap %s" % (cmp_op, op))
      func.opcodes[i] = opcode
      i += 1

class ModifyConstantMutation(MutationOp):
  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    myconsts = set()
    while i < len(func.opcodes):
      opcode = func.opcodes[i]
      if opcode.name == 'LOAD_CONST':
        c = opcode.arg() - 1 # - docstring
        if c not in myconsts:
          myconsts.add(c)
          # get where the const is loading it from.
          const = func.consts[c]
          # Mess with ints
          if isinstance(const, int):
            func.consts[c] = const + 1
            yield (func.build(), opcode.lineno, "mcm, %d : +1" % const)

            func.consts[c] = const - 1
            yield (func.build(), opcode.lineno, "mcm, %d : -1" % const)

            r = 0
            if const == 0:
              r = 1
            func.consts[c] = r
            yield (func.build(), opcode.lineno, "mcm, %d : swap %d" % (const, r))

          func.consts[c] = const
      func.opcodes[i] = opcode
      i += 1

class UnaryMutation(MutationOp):
  _un_table = {'UNARY_POSITIVE': 'UNARY_NEGATIVE',
               'UNARY_NEGATIVE': 'UNARY_POSITIVE',
               'UNARY_NOT':      'NOP',
               'UNARY_INVERT':   'NOP'
               }

  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]

      other = self._un_table.get(opcode.name)
      if other:
        new_opcode = opobj.Opcode(dis.opmap[other], opcode.lineno, opcode.arg1, opcode.arg2)
        func.opcodes[i] = new_opcode
        yield (func.build(), opcode.lineno, "um, %s : swap %s" % (opcode.name, other))

      func.opcodes[i] = opcode
      i += 1

class SwapOpsTemplate(MutationOp):
  def __init__(self, names, msg):
    self.names, self.msg = names, msg
  def mutants(self, function):
    ops = self.names.keys()
    allpairs = [(o,o1) for o in ops for o1 in ops if o != o1]

    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]
      codes = [j[1] for j in allpairs if j[0] == opcode.name]
      for other in codes:
        new_opcode = opobj.Opcode(dis.opmap[other], opcode.lineno, opcode.arg1, opcode.arg2)
        func.opcodes[i] = new_opcode
        yield (func.build(), opcode.lineno, self.msg % (self.names[opcode.name], self.names[other]))

      func.opcodes[i] = opcode
      i += 1

def allm():
  inplaceMutationRelational = SwapOpsTemplate({'INPLACE_AND':'&&', 'INPLACE_OR':'||'}, "imr, %s : swap %s")
  inplaceMutationNum = SwapOpsTemplate({'INPLACE_FLOOR_DIVIDE':'//=', 'INPLACE_TRUE_DIVIDE':'./=.', 'INPLACE_DIVIDE':'/=', 'INPLACE_MULTIPLY':'*=', 'INPLACE_POWER':'**=', 'INPLACE_MODULO':'%=', 'INPLACE_ADD':'+=', 'INPLACE_SUBTRACT':'-=', 'INPLACE_LSHIFT':'<<=', 'INPLACE_RSHIFT':'>>=', 'INPLACE_XOR':'^='}, "imn, %s : swap %s")
  jumpMutationStack2 = SwapOpsTemplate({'JUMP_IF_TRUE_OR_POP':'if_true_or_pop', 'JUMP_IF_FALSE_OR_POP':'if_false_or_pop'}, "jms2, %s : swap %s")
  jumpMutationStack = SwapOpsTemplate({'POP_JUMP_IF_TRUE':'pop_if_true', 'POP_JUMP_IF_FALSE':'pop_if_false'}, "jms, %s : swap %s")
  binaryMutationRelational = SwapOpsTemplate({'BINARY_AND':'&&', 'BINARY_OR':'||'}, "bmr, %s : swap %s")
  binaryMutationNum = SwapOpsTemplate({'BINARY_FLOOR_DIVIDE':'//', 'BINARY_TRUE_DIVIDE':'./.', 'BINARY_DIVIDE':'/', 'BINARY_MULTIPLY':'*', 'BINARY_POWER':'**', 'BINARY_MODULO':'%', 'BINARY_ADD':'+', 'BINARY_SUBTRACT':'-', 'BINARY_LSHIFT':'<<', 'BINARY_RSHIFT':'>>', 'BINARY_XOR':'^'}, "bmn, %s : swap %s")
  return [BoolComparisonMutation(),
          SetComparisonMutation(),
          ModifyConstantMutation(),
          jumpMutationStack,
          jumpMutationStack2,
          UnaryMutation(),
          binaryMutationNum,
          binaryMutationRelational,
          inplaceMutationNum,
          inplaceMutationRelational]

# NOP DUP_TOP POP_TOP
# ROT_TWO ROT_THREE ROT_FOUR
# 
# UNARY_POSITIVE UNARY_NEGATIVE UNARY_NOT UNARY_INVERT
# 
# BINARY_POWER BINARY_MULTIPLY BINARY_FLOOR_DIVIDE BINARY_TRUE_DIVIDE
# BINARY_MODULO BINARY_ADD BINARY_SUBTRACT
# BINARY_LSHIFT BINARY_RSHIFT 
# 
# BINARY_AND BINARY_XOR BINARY_OR 
# 
# INPLACE_POWER INPLACE_MULTIPLY INPLACE_FLOOR_DIVIDE INPLACE_TRUE_DIVIDE INPLACE_MODULO
# INPLACE_ADD INPLACE_SUBTRACT 
# INPLACE_LSHIFT INPLACE_RSHIFT
# 
# INPLACE_AND INPLACE_XOR INPLACE_OR
# 
# BREAK_LOOP CONTINUE_LOOP(tgt)
# 
# RETURN_VALUE
# 
# POP_JUMP_IF_TRUE(target)
# POP_JUMP_IF_FALSE(target)
# 
# JUMP_IF_TRUE_OR_POP(target)
# JUMP_IF_FALSE_OR_POP(target)
# 
# JUMP_ABSOLUTE(target)

