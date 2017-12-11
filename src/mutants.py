import fn
import mutator
import dis


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

    >>> myfn(2)
    True
    >>> mutantfn(2)
    False

    >>> myfn.__code__.co_consts
    (None, 1, True, False)
    >>> [int(i) for i in myfn.__code__.co_code]
    [124, 0, 100, 1, 107, 4, 114, 12, 100, 2, 83, 0, 100, 3, 83, 0, 100, 0, 83, 0]
    >>> [int(i) for i in mutantfn.__code__.co_code]
    [124, 0, 100, 1, 107, 4, 114, 12, 100, 2, 83, 0, 100, 3, 83, 0, 100, 0, 83, 0]
    >>> mutantfn.__code__.co_consts
    (None, 2, True, False)

    Ensure we had no modification in code. Only in constants

    >>> dis.dis(myfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE       12
              8 LOAD_CONST               2 (2)
             10 RETURN_VALUE
        >>   12 LOAD_CONST               3 (3)
             14 RETURN_VALUE
             16 LOAD_CONST               0 (0)
             18 RETURN_VALUE
    >>> dis.dis(mutantfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE       12
              8 LOAD_CONST               2 (2)
             10 RETURN_VALUE
        >>   12 LOAD_CONST               3 (3)
             14 RETURN_VALUE
             16 LOAD_CONST               0 (0)
             18 RETURN_VALUE
    """

    def mutants(self, function):
        lst = []
        func = fn.Function(function)
        myconsts = set()
        for i, opcode in enumerate(func.opcodes):
            index = 0
            if opcode.opname == 'LOAD_CONST':
                c = opcode.arg - 1
                if c not in myconsts:
                    myconsts.add(c)
                    # get where the const is loading it from.
                    if c < 0: continue
                    const = func.consts[c]
                    if type(const) is int:
                        func.consts[c] = const + 1
                        lst.append((func.build(), opcode.starts_line, i, index, "mcm, %d : +1" % const))
                        index += 1

                        func.consts[c] = const - 1
                        lst.append((func.build(), opcode.starts_line, i, index, "mcm, %d : -1" % const))
                        index += 1

                        if const != 0:
                            func.consts[c] = const * -1
                            lst.append((func.build(), opcode.starts_line, i, index, "mcm, %d : swap -%d" % (const, const)))
                            index += 1

                    func.consts[c] = const
            func.opcodes[i] = opcode
        return lst


class ComparisonTemplate(MutationOp):
    """
    >>> def myfn(x):
    ...   if x > 1:
    ...       return True
    ...   else:
    ...       return False
    >>> mym = ComparisonTemplate( ['<', '>'], "bcm, %s : swap %s")
    >>> [(mutantfn, l, i, index, m)] = mym.mutants(myfn)
 
    >>> myfn(0)
    False
    >>> mutantfn(0)
    True
 
    >>> [int(i) for i in myfn.__code__.co_code]
    [124, 0, 100, 1, 107, 4, 114, 12, 100, 2, 83, 0, 100, 3, 83, 0, 100, 0, 83, 0]
    >>> [int(i) for i in mutantfn.__code__.co_code]
    [124, 0, 100, 1, 107, 0, 114, 12, 100, 2, 83, 0, 100, 3, 83, 0, 100, 0, 83, 0]
    >>> dis.dis(myfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE       12
              8 LOAD_CONST               2 (2)
             10 RETURN_VALUE
        >>   12 LOAD_CONST               3 (3)
             14 RETURN_VALUE
             16 LOAD_CONST               0 (0)
             18 RETURN_VALUE
    >>> dis.dis(mutantfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               0 (<)
              6 POP_JUMP_IF_FALSE       12
              8 LOAD_CONST               2 (2)
             10 RETURN_VALUE
        >>   12 LOAD_CONST               3 (3)
             14 RETURN_VALUE
             16 LOAD_CONST               0 (0)
             18 RETURN_VALUE
    >>> def myfn(x):
    ...   if x >= 1:
    ...       return True
    ...   else:
    ...       return False
 
    >>> mym = ComparisonTemplate( ['>', '>='], "bcm, %s : swap %s")
 
    >>> [int(i) for i in myfn.__code__.co_code]
    [124, 0, 100, 1, 107, 5, 114, 12, 100, 2, 83, 0, 100, 3, 83, 0, 100, 0, 83, 0]
    >>> [(mutantfn, l, i, index, m)] = mym.mutants(myfn)
 
    >>> myfn(1)
    True
    >>> mutantfn(1)
    False
 
    >>> [int(i) for i in mutantfn.__code__.co_code]
    [124, 0, 100, 1, 107, 4, 114, 12, 100, 2, 83, 0, 100, 3, 83, 0, 100, 0, 83, 0]
    >>> dis.dis(myfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               5 (>=)
              6 POP_JUMP_IF_FALSE       12
              8 LOAD_CONST               2 (2)
             10 RETURN_VALUE
        >>   12 LOAD_CONST               3 (3)
             14 RETURN_VALUE
             16 LOAD_CONST               0 (0)
             18 RETURN_VALUE
    >>> dis.dis(mutantfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE       12
              8 LOAD_CONST               2 (2)
             10 RETURN_VALUE
        >>   12 LOAD_CONST               3 (3)
             14 RETURN_VALUE
             16 LOAD_CONST               0 (0)
             18 RETURN_VALUE
    """

    def __init__(self, myops, msg):
        self.myops, self.msg = myops, msg

    def mutants(self, function):
        func = fn.Function(function)
        lst = []
        for i, opcode in enumerate(func.opcodes):
            arg = func.args[i]
            index = 0

            if opcode.opname == 'COMPARE_OP':
                cmp_op = dis.cmp_op[opcode.arg]
                if cmp_op in self.myops:
                    for op in self.myops:
                        if cmp_op != op:
                            n = dis.cmp_op.index(op)
                            new_arg = dis.cmp_op.index(op)
                            func.args[i] = new_arg
                            lst.append((func.build(), opcode.starts_line, i, index, self.msg % (cmp_op, op)))
                            index += 1
            func.opcodes[i] = opcode
        return lst


class KillOpTemplate(MutationOp):
    """
    >>> def myfn(x):
    ...   return not(x)
    >>> mym = KillOpTemplate( {'UNARY_NOT': 'NOP'}, "um, %s : swap %s")
    >>> (mutantfn, l, i, index, m) = list(mym.mutants(myfn))[0]
 
    >>> myfn(True)
    False
    >>> mutantfn(True)
    True
 
    >>> [int(i) for i in myfn.__code__.co_code]
    [124, 0, 12, 0, 83, 0]
    >>> [int(i) for i in mutantfn.__code__.co_code]
    [124, 0, 9, 0, 83, 0]
    >>> dis.dis(myfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 UNARY_NOT
              4 RETURN_VALUE
    >>> dis.dis(mutantfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 NOP
              4 RETURN_VALUE
    """

    def __init__(self, names, msg):
        self.optable, self.msg = names, msg

    def mutants(self, function):
        func = fn.Function(function)
        lst = []
        for i,opcode in enumerate(func.opcodes):
            opcode = func.opcodes[i]
            index = 0

            other = self.optable.get(opcode.opname)
            if other:
                new_op = dis.opmap[other]
                func.ops[i] = new_op
                lst.append((func.build(), opcode.starts_line, i, index, self.msg % (opcode.opname, other)))
                index += 1

            func.opcodes[i] = opcode
        return lst


class SwapOpsTemplate(MutationOp):
    """
    >>> def myfn(x):
    ...   return x + 1
    >>> mym = SwapOpsTemplate( {'BINARY_ADD': '+', 'BINARY_SUBTRACT':'-'}, "bmn, %s : swap %s")
    >>> (mutantfn, l, i, index, m) = list(mym.mutants(myfn))[0]
 
    >>> myfn(1)
    2
    >>> mutantfn(1)
    0
 
    >>> [int(i) for i in myfn.__code__.co_code]
    [124, 0, 100, 1, 23, 0, 83, 0]
    >>> [int(i) for i in mutantfn.__code__.co_code]
    [124, 0, 100, 1, 24, 0, 83, 0]
    >>> myfn(1)
    2
    >>> mutantfn(1)
    0
    >>> dis.dis(myfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 BINARY_ADD
              6 RETURN_VALUE
    >>> dis.dis(mutantfn.__code__.co_code)
              0 LOAD_FAST                0 (0)
              2 LOAD_CONST               1 (1)
              4 BINARY_SUBTRACT
              6 RETURN_VALUE
    """

    def __init__(self, names, msg):
        self.names, self.msg = names, msg

    def mutants(self, function):
        ops = self.names.keys()
        allpairs = [(o, o1) for o in ops for o1 in ops if o != o1]
        lst = []

        func = fn.Function(function)
        for i, opcode in enumerate(func.opcodes):
            index = 0
            codes = [j[1] for j in allpairs if j[0] == opcode.opname]
            for other in codes:
                func.ops[i] = dis.opmap[other]
                lst.append((func.build(), opcode.starts_line, i, index, self.msg % (self.names[opcode.opname], self.names[other])))
                index += 1
        return lst


def allm():
    unaryNot = KillOpTemplate({'UNARY_NOT': 'NOP', 'UNARY_INVERT': 'NOP'}, "um, %s : swap %s")
    unarySign = SwapOpsTemplate({'UNARY_POSITIVE': '+u', 'UNARY_NEGATIVE': '-u'}, "us, %s : swap %s")
    inplaceMutationRelational = SwapOpsTemplate({'INPLACE_AND': '&&', 'INPLACE_OR': '||'}, "imr, %s : swap %s")
    inplaceMutationNum = SwapOpsTemplate(
        {'INPLACE_FLOOR_DIVIDE': '//=', 'INPLACE_TRUE_DIVIDE': './=.', 'INPLACE_TRUE_DIVIDE': '/=', 'INPLACE_MULTIPLY': '*=',
         'INPLACE_POWER': '**=', 'INPLACE_MODULO': '%=', 'INPLACE_ADD': '+=', 'INPLACE_SUBTRACT': '-=',
         'INPLACE_LSHIFT': '<<=', 'INPLACE_RSHIFT': '>>=', 'INPLACE_XOR': '^='}, "imn, %s : swap %s")
    jumpMutationStack2 = SwapOpsTemplate(
        {'JUMP_IF_TRUE_OR_POP': 'if_true_or_pop', 'JUMP_IF_FALSE_OR_POP': 'if_false_or_pop'}, "jmsp, %s : swap %s")
    jumpMutationStack = SwapOpsTemplate({'POP_JUMP_IF_TRUE': 'pop_if_true', 'POP_JUMP_IF_FALSE': 'pop_if_false'},
                                        "jms, %s : swap %s")
    binaryMutationRelational = SwapOpsTemplate({'BINARY_AND': '&&', 'BINARY_OR': '||'}, "bmr, %s : swap %s")
    binaryMutationNum = SwapOpsTemplate(
        {'BINARY_FLOOR_DIVIDE': '//', 'BINARY_TRUE_DIVIDE': './.', 'BINARY_TRUE_DIVIDE': '/', 'BINARY_MULTIPLY': '*',
         'BINARY_POWER': '**', 'BINARY_MODULO': '%', 'BINARY_ADD': '+', 'BINARY_SUBTRACT': '-', 'BINARY_LSHIFT': '<<',
         'BINARY_RSHIFT': '>>', 'BINARY_XOR': '^'}, "bmn, %s : swap %s")

    boolComparisonMutation = ComparisonTemplate(['<', '<=', '==', '!=', '>', '>='], "bcm, %s : swap %s")
    setComparisonMutation = ComparisonTemplate(['in', 'not in'], "scm, %s : swap %s")
    return map(mutator.Mutator, [boolComparisonMutation,
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

# Two mutations were
# based on mutant by "Michael Stephens <me@mikej.st>" BSD License
