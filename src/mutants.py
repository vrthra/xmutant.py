import fn
import mutator
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

class ModifyIntConstantMutation(MutationOp):
  """
  >>> def myfn(x):
  ...   if x > 1:
  ...       return True
  ...   else:
  ...       return False
  >>> mym = ModifyIntConstantMutation()
  >>> (mutantfn, l, i, index, m) = list(mym.mutants(myfn))[0]
  >>> myfn.func_code.co_consts
  (None, 1)
  >>> [ord(i) for i in myfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 107, 4, 0, 114, 16, 0, 116, 0, 0, 83, 116, 1, 0, 83, 100, 0, 0, 83]
  >>> [ord(i) for i in mutantfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 107, 4, 0, 114, 16, 0, 116, 0, 0, 83, 116, 1, 0, 83, 100, 0, 0, 83]
  >>> mutantfn.func_code.co_consts
  (None, 2)
  >>> myfn(2)
  True
  >>> mutantfn(2)
  False
  >>> dis.dis(myfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 COMPARE_OP          4 (>)
            9 POP_JUMP_IF_FALSE    16
           12 LOAD_GLOBAL         0 (0)
           15 RETURN_VALUE   
      >>   16 LOAD_GLOBAL         1 (1)
           19 RETURN_VALUE   
           20 LOAD_CONST          0 (0)
           23 RETURN_VALUE   
  >>> dis.dis(mutantfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 COMPARE_OP          4 (>)
            9 POP_JUMP_IF_FALSE    16
           12 LOAD_GLOBAL         0 (0)
           15 RETURN_VALUE   
      >>   16 LOAD_GLOBAL         1 (1)
           19 RETURN_VALUE   
           20 LOAD_CONST          0 (0)
           23 RETURN_VALUE   
  """

  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    myconsts = set()
    while i < len(func.opcodes):
      opcode = func.opcodes[i]
      index = 0
      if opcode.name == 'LOAD_CONST':
        c = opcode.arg() - 1 # - docstring
        if c not in myconsts:
          myconsts.add(c)
          # get where the const is loading it from.
          if c < 0: continue
          const = func.consts[c]
          if isinstance(const, int):
            func.consts[c] = const + 1
            yield (func.build(), opcode.lineno, i, index, "mcm, %d : +1" % const)
            index += 1

            func.consts[c] = const - 1
            yield (func.build(), opcode.lineno, i, index, "mcm, %d : -1" % const)
            index += 1

            if const != 0:
              func.consts[c] = const * -1
              yield (func.build(), opcode.lineno, i, index, "mcm, %d : swap -%d" % (const, const))
              index += 1

          func.consts[c] = const
      func.opcodes[i] = opcode
      i += 1

class ComparisonTemplate(MutationOp):
  """
  >>> def myfn(x):
  ...   if x > 1:
  ...       return True
  ...   else:
  ...       return False
  >>> mym = ComparisonTemplate( ['<', '>'], "bcm, %s : swap %s")
  >>> [(mutantfn, l, i, index, m)] = mym.mutants(myfn)
  >>> [ord(i) for i in myfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 107, 4, 0, 114, 16, 0, 116, 0, 0, 83, 116, 1, 0, 83, 100, 0, 0, 83]
  >>> [ord(i) for i in mutantfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 107, 0, 0, 114, 16, 0, 116, 0, 0, 83, 116, 1, 0, 83, 100, 0, 0, 83]
  >>> myfn(0)
  False
  >>> mutantfn(0)
  True
  >>> dis.dis(myfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 COMPARE_OP          4 (>)
            9 POP_JUMP_IF_FALSE    16
           12 LOAD_GLOBAL         0 (0)
           15 RETURN_VALUE   
      >>   16 LOAD_GLOBAL         1 (1)
           19 RETURN_VALUE   
           20 LOAD_CONST          0 (0)
           23 RETURN_VALUE   
  >>> dis.dis(mutantfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 COMPARE_OP          0 (<)
            9 POP_JUMP_IF_FALSE    16
           12 LOAD_GLOBAL         0 (0)
           15 RETURN_VALUE   
      >>   16 LOAD_GLOBAL         1 (1)
           19 RETURN_VALUE   
           20 LOAD_CONST          0 (0)
           23 RETURN_VALUE   
  >>> def myfn(x):
  ...   if x >= 1:
  ...       return True
  ...   else:
  ...       return False

  >>> mym = ComparisonTemplate( ['>', '>='], "bcm, %s : swap %s")
  >>> [ord(i) for i in myfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 107, 5, 0, 114, 16, 0, 116, 0, 0, 83, 116, 1, 0, 83, 100, 0, 0, 83]
  >>> [(mutantfn, l, i, index, m)] = mym.mutants(myfn)
  >>> [ord(i) for i in mutantfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 107, 4, 0, 114, 16, 0, 116, 0, 0, 83, 116, 1, 0, 83, 100, 0, 0, 83]
  >>> myfn(1)
  True
  >>> mutantfn(1)
  False
  >>> dis.dis(myfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 COMPARE_OP          5 (>=)
            9 POP_JUMP_IF_FALSE    16
           12 LOAD_GLOBAL         0 (0)
           15 RETURN_VALUE   
      >>   16 LOAD_GLOBAL         1 (1)
           19 RETURN_VALUE   
           20 LOAD_CONST          0 (0)
           23 RETURN_VALUE   
  >>> dis.dis(mutantfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 COMPARE_OP          4 (>)
            9 POP_JUMP_IF_FALSE    16
           12 LOAD_GLOBAL         0 (0)
           15 RETURN_VALUE   
      >>   16 LOAD_GLOBAL         1 (1)
           19 RETURN_VALUE   
           20 LOAD_CONST          0 (0)
           23 RETURN_VALUE   
  """
  def __init__(self, myops, msg):
    self.myops, self.msg = myops, msg

  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]
      index = 0

      if opcode.name == 'COMPARE_OP':
        cmp_op = dis.cmp_op[opcode.arg()]
        if cmp_op in self.myops:
          for op in self.myops:
            if cmp_op != op:
              n = dis.cmp_op.index(op)
              new_oc = opobj.Opcode(opcode.opcode, opcode.lineno, n & 255, n >> 8)
              func.opcodes[i] = new_oc
              yield (func.build(), opcode.lineno, i, index, self.msg % (cmp_op, op))
              index += 1
      func.opcodes[i] = opcode
      i += 1

class KillOpTemplate(MutationOp):
  """
  >>> def myfn(x):
  ...   return not(x)
  >>> mym = KillOpTemplate( {'UNARY_NOT': 'NOP'}, "um, %s : swap %s")
  >>> (mutantfn, l, i, index, m) = list(mym.mutants(myfn))[0]
  >>> [ord(i) for i in myfn.func_code.co_code]
  [124, 0, 0, 12, 83]
  >>> [ord(i) for i in mutantfn.func_code.co_code]
  [124, 0, 0, 9, 83]
  >>> myfn(True)
  False
  >>> mutantfn(True)
  True
  >>> dis.dis(myfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 UNARY_NOT      
            4 RETURN_VALUE   
  >>> dis.dis(mutantfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 NOP            
            4 RETURN_VALUE   
  """
  def __init__(self, names, msg):
    self.optable, self.msg = names, msg

  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]
      index = 0

      other = self.optable.get(opcode.name)
      if other:
        new_opcode = opobj.Opcode(dis.opmap[other], opcode.lineno, opcode.arg1, opcode.arg2)
        func.opcodes[i] = new_opcode
        yield (func.build(), opcode.lineno, i, index, self.msg % (opcode.name, other))
        index += 1

      func.opcodes[i] = opcode
      i += 1

class SwapOpsTemplate(MutationOp):
  """
  >>> def myfn(x):
  ...   return x + 1
  >>> mym = SwapOpsTemplate( {'BINARY_ADD': '+', 'BINARY_SUBTRACT':'-'}, "bmn, %s : swap %s")
  >>> (mutantfn, l, i, index, m) = list(mym.mutants(myfn))[0]
  >>> [ord(i) for i in myfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 23, 83]
  >>> [ord(i) for i in mutantfn.func_code.co_code]
  [124, 0, 0, 100, 1, 0, 24, 83]
  >>> myfn(1)
  2
  >>> mutantfn(1)
  0
  >>> dis.dis(myfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 BINARY_ADD     
            7 RETURN_VALUE   
  >>> dis.dis(mutantfn.func_code.co_code)
            0 LOAD_FAST           0 (0)
            3 LOAD_CONST          1 (1)
            6 BINARY_SUBTRACT
            7 RETURN_VALUE   
  """
  def __init__(self, names, msg):
    self.names, self.msg = names, msg
  def mutants(self, function):
    ops = self.names.keys()
    allpairs = [(o,o1) for o in ops for o1 in ops if o != o1]

    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]
      index = 0
      codes = [j[1] for j in allpairs if j[0] == opcode.name]
      for other in codes:
        new_opcode = opobj.Opcode(dis.opmap[other], opcode.lineno, opcode.arg1, opcode.arg2)
        func.opcodes[i] = new_opcode
        yield (func.build(), opcode.lineno, i, index, self.msg % (self.names[opcode.name], self.names[other]))
        index += 1

      func.opcodes[i] = opcode
      i += 1

def allm():
  unaryNot = KillOpTemplate({'UNARY_NOT': 'NOP', 'UNARY_INVERT':'NOP'}, "um, %s : swap %s")
  unarySign = SwapOpsTemplate({'UNARY_POSITIVE':'+u', 'UNARY_NEGATIVE':'-u'}, "us, %s : swap %s")
  inplaceMutationRelational = SwapOpsTemplate({'INPLACE_AND':'&&', 'INPLACE_OR':'||'}, "imr, %s : swap %s")
  inplaceMutationNum = SwapOpsTemplate({'INPLACE_FLOOR_DIVIDE':'//=', 'INPLACE_TRUE_DIVIDE':'./=.', 'INPLACE_DIVIDE':'/=', 'INPLACE_MULTIPLY':'*=', 'INPLACE_POWER':'**=', 'INPLACE_MODULO':'%=', 'INPLACE_ADD':'+=', 'INPLACE_SUBTRACT':'-=', 'INPLACE_LSHIFT':'<<=', 'INPLACE_RSHIFT':'>>=', 'INPLACE_XOR':'^='}, "imn, %s : swap %s")
  jumpMutationStack2 = SwapOpsTemplate({'JUMP_IF_TRUE_OR_POP':'if_true_or_pop', 'JUMP_IF_FALSE_OR_POP':'if_false_or_pop'}, "jmsp, %s : swap %s")
  jumpMutationStack = SwapOpsTemplate({'POP_JUMP_IF_TRUE':'pop_if_true', 'POP_JUMP_IF_FALSE':'pop_if_false'}, "jms, %s : swap %s")
  binaryMutationRelational = SwapOpsTemplate({'BINARY_AND':'&&', 'BINARY_OR':'||'}, "bmr, %s : swap %s")
  binaryMutationNum = SwapOpsTemplate({'BINARY_FLOOR_DIVIDE':'//', 'BINARY_TRUE_DIVIDE':'./.', 'BINARY_DIVIDE':'/', 'BINARY_MULTIPLY':'*', 'BINARY_POWER':'**', 'BINARY_MODULO':'%', 'BINARY_ADD':'+', 'BINARY_SUBTRACT':'-', 'BINARY_LSHIFT':'<<', 'BINARY_RSHIFT':'>>', 'BINARY_XOR':'^'}, "bmn, %s : swap %s")

  boolComparisonMutation = ComparisonTemplate( ['<', '<=', '==', '!=', '>', '>='], "bcm, %s : swap %s")
  setComparisonMutation = ComparisonTemplate( ['in', 'not in'], "scm, %s : swap %s")
  return map(mutator.Mutator,[boolComparisonMutation,
          setComparisonMutation,
          ModifyIntConstantMutation(),
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

