# vim: set nospell:
import dis
import doctest
import opobj
import fn

def runAllTests(module, first=True):
  """
  Run all of a modules doctests, not producing any output to stdout.
  Return a tuple with the number of failures and the number of tries.
  """
  finder = doctest.DocTestFinder(exclude_empty=False)
  runner = doctest.DocTestRunner(verbose=False)
  for test in finder.find(module, module.__name__):
    runner.run(test, out=lambda x: True)
    if first and runner.failures > 0:
      return runner.failures
  return runner.failures

class MutationOp(object):
  def __init__(self):
    pass

  def runTests(self, module, function, not_covered):
    fail_count = 0
    mutant_count = 0
    skipped = 0

    for mutant_func, line, msg in self.mutants(function):
      mutant_count += 1
      if line in not_covered:
        skipped += 1
      else:
        setattr(module, function.func_name, mutant_func)
        detected = runAllTests(module, first=True)

        if detected == 0:
          print "\tX: %s.%s %s" % (module.__name__, function.func_name, msg)
          fail_count += 1

    # Restore original function
    setattr(module, function.func_name, function)

    return (fail_count, skipped, mutant_count)

  def mutants(self, function):
    """
    MutationOps should override this to return an iterator of
    mutated functions.
    """
    raise NotImplementedError()


class ComparisonMutation(MutationOp):
  """
  Swap comparsion operators (e.g. change '>' to '>=' or '==')
  """

  def mutants(self, function):
    func = fn.Function(function)

    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]

      if opcode.name == 'COMPARE_OP':
        cmp_op = dis.cmp_op[opcode.arg()]

        for op in dis.cmp_op:
          if not op in [cmp_op, 'exception match', 'BAD']:
            n = dis.cmp_op.index(op)
            new_oc = opobj.Opcode(opcode.opcode, opcode.lineno,
                    n >> 8, n & 255)
            func.opcodes[i] = new_oc
            yield (func.build(), opcode.lineno, "changed %s to %s" % (cmp_op, op))

        # Reset opcode
        func.opcodes[i] = opcode

      # Next opcode
      i += 1


class ModifyConstantMutation(MutationOp):
  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    while i < len(func.consts):
      const = func.consts[i]

      # Should cause test failure if a non-None const is set to None
      if const is not None:
        func.consts[i] = None
        yield (func.build(), -1, "replaced %s with None" % const)

      # Mess with ints
      if isinstance(const, int):
        func.consts[i] = const + 1
        yield (func.build(), -1, "%d : +1" % const)

        func.consts[i] = const - 1
        yield (func.build(), -1, "%d : -1" % const)

        r = 0
        func.consts[i] = r
        yield (func.build(), -1, "%d : swap %d" % (const, r))

      # Reset const
      func.consts[i] = const

      # Next const
      i += 1


class JumpMutation(MutationOp):
  _jump_table = {'JUMP_IF_TRUE': 'JUMP_IF_FALSE',
                 'JUMP_IF_FALSE': 'JUMP_IF_TRUE'}

  def mutants(self, function):
    func = fn.Function(function)
    i = 0
    while i < len(func.opcodes):
      opcode = func.opcodes[i]

      other_jump = self._jump_table.get(opcode.name)
      if other_jump:
        new_opcode = opobj.Opcode(dis.opmap[other_jump], opcode.lineno,
                  opcode.arg1, opcode.arg2)
        func.opcodes[i] = new_opcode
        yield (func.build(), opcode.lineno, "<line:%d> : negated jump" % new_opcode.lineno)

        # Reset opcode
        func.opcodes[i] = opcode

      # Next opcode
      i += 1

