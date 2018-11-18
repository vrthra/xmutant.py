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
    def mutants(self, function):
        lst = []
        func = mutator.Function(function)
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
    def __init__(self, myops, msg):
        self.myops, self.msg = myops, msg

    def mutants(self, function):
        func = mutator.Function(function)
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
    def __init__(self, names, msg):
        self.optable, self.msg = names, msg

    def mutants(self, function):
        func = mutator.Function(function)
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
    def __init__(self, names, msg):
        self.names, self.msg = names, msg

    def mutants(self, function):
        ops = self.names.keys()
        allpairs = [(o, o1) for o in ops for o1 in ops if o != o1]
        lst = []

        func = mutator.Function(function)
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

# Two mutations were
# based on mutant by "Michael Stephens <me@mikej.st>" BSD License
