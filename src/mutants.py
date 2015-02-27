import fn
import mutators
import dis
import opobj

class MutationOp(object):
  def __init__(self):
    pass

  def mutants(self, function):
    """
    MutationOps should override this to return an iterator of
    mutated functions.
    """
    raise NotImplementedError()

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

class ComparisonTemplate(MutationOp):
  def __init__(self, myops, msg):
    self.myops, self.msg = myops, msg

  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]

      if opcode.name == 'COMPARE_OP':
        cmp_op = dis.cmp_op[opcode.arg()]
        if cmp_op in self.myops:
          for op in self.myops:
            if cmp_op != op:
              n = dis.cmp_op.index(op)
              new_oc = opobj.Opcode(opcode.opcode, opcode.lineno, n >> 8, n & 255)
              func.opcodes[i] = new_oc
              yield (func.build(), opcode.lineno, self.msg % (cmp_op, op))
      func.opcodes[i] = opcode
      i += 1

class KillOpTemplate(MutationOp):
  def __init__(self, names, msg):
    self.optable, self.msg = names, msg

  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]

      other = self.optable.get(opcode.name)
      if other:
        new_opcode = opobj.Opcode(dis.opmap[other], opcode.lineno, opcode.arg1, opcode.arg2)
        func.opcodes[i] = new_opcode
        yield (func.build(), opcode.lineno, self.msg % (opcode.name, other))

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
  unaryNot = KillOpTemplate({'UNARY_NOT': 'NOP', 'UNARY_INVERT':'NOP'}, "um, %s : swap %s")
  unarySign = SwapOpsTemplate({'UNARY_POSITIVE':'+u', 'UNARY_NEGATIVE':'-u'}, "us, %s : swap %s")
  inplaceMutationRelational = SwapOpsTemplate({'INPLACE_AND':'&&', 'INPLACE_OR':'||'}, "imr, %s : swap %s")
  inplaceMutationNum = SwapOpsTemplate({'INPLACE_FLOOR_DIVIDE':'//=', 'INPLACE_TRUE_DIVIDE':'./=.', 'INPLACE_DIVIDE':'/=', 'INPLACE_MULTIPLY':'*=', 'INPLACE_POWER':'**=', 'INPLACE_MODULO':'%=', 'INPLACE_ADD':'+=', 'INPLACE_SUBTRACT':'-=', 'INPLACE_LSHIFT':'<<=', 'INPLACE_RSHIFT':'>>=', 'INPLACE_XOR':'^='}, "imn, %s : swap %s")
  jumpMutationStack2 = SwapOpsTemplate({'JUMP_IF_TRUE_OR_POP':'if_true_or_pop', 'JUMP_IF_FALSE_OR_POP':'if_false_or_pop'}, "jms2, %s : swap %s")
  jumpMutationStack = SwapOpsTemplate({'POP_JUMP_IF_TRUE':'pop_if_true', 'POP_JUMP_IF_FALSE':'pop_if_false'}, "jms, %s : swap %s")
  binaryMutationRelational = SwapOpsTemplate({'BINARY_AND':'&&', 'BINARY_OR':'||'}, "bmr, %s : swap %s")
  binaryMutationNum = SwapOpsTemplate({'BINARY_FLOOR_DIVIDE':'//', 'BINARY_TRUE_DIVIDE':'./.', 'BINARY_DIVIDE':'/', 'BINARY_MULTIPLY':'*', 'BINARY_POWER':'**', 'BINARY_MODULO':'%', 'BINARY_ADD':'+', 'BINARY_SUBTRACT':'-', 'BINARY_LSHIFT':'<<', 'BINARY_RSHIFT':'>>', 'BINARY_XOR':'^'}, "bmn, %s : swap %s")

  boolComparisonMutation = ComparisonTemplate( ['<', '<=', '==', '!=', '>', '>='], "bcm, %s : swap %s")
  setComparisonMutation = ComparisonTemplate( ['in', 'not in'], "scm, %s : swap %s")
  return map(mutators.Mutator,[boolComparisonMutation,
          setComparisonMutation,
          ModifyConstantMutation(),
          unarySign,
          jumpMutationStack,
          jumpMutationStack2,
          unaryNot,
          binaryMutationNum,
          binaryMutationRelational,
          inplaceMutationNum,
          inplaceMutationRelational])

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

