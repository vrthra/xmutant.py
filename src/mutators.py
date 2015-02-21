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
    myargs = ''.join([e.source for e in test.examples if e.source.startswith('args = ')])
    if myargs.strip() != '':
      loc, glob = {}, {}
      args = eval(myargs[7:], glob, loc)
      mymax = args[0]['max']
      mymin = args[0]['min']
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
        print "\t_: %s.%s %s" % (module.__name__, function.func_name, msg)
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
          # Should cause test failure if a non-None const is set to None
          if const is not None:
            func.consts[c] = None
            yield (func.build(), opcode.lineno, "replaced %s with None" % const)

          # Mess with ints
          if isinstance(const, int):
            func.consts[c] = const + 1
            yield (func.build(), opcode.lineno, "%d : +1" % const)

            func.consts[c] = const - 1
            yield (func.build(), opcode.lineno, "%d : -1" % const)

            r = 0
            func.consts[c] = r
            yield (func.build(), opcode.lineno, "%d : swap %d" % (const, r))

          func.consts[c] = const
      func.opcodes[i] = opcode
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

      func.opcodes[i] = opcode
      i += 1

