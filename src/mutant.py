#!/usr/bin/env python
# vim: set nospell:
import sys
import dis
import random
import inspect
import doctest
import coverage
import opobj
import fn

class MutationOp(object):
  def __init__(self, stop_on_fail=False):
    self.stop_on_fail = stop_on_fail

  def runTests(self, module, function):
    pass_count = 0
    mutant_count = 0

    for mutant_func, line, msg in self.mutants(function):
      setattr(module, function.func_name, mutant_func)
      fails = runAllTests(module)[0]

      mutant_count += 1

      if fails == 0:
        print "\tX: %s.%s %s" % (module.__name__, function.func_name, msg)
        pass_count += 1

        if self.stop_on_fail: break

    # Restore original function
    setattr(module, function.func_name, function)

    return (pass_count, mutant_count)

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

def runAllTests(module):
  """
  Run all of a modules doctests, not producing any output to stdout.
  Return a tuple with the number of failures and the number of tries.
  """
  finder = doctest.DocTestFinder(exclude_empty=False)
  runner = doctest.DocTestRunner(verbose=False)
  for test in finder.find(module, module.__name__):
    runner.run(test, out=lambda x: True)
  return (runner.failures, runner.tries)


def runAllTestsCov(module):
  """
  Run all of a modules doctests, not producing any output to stdout.
  Return a tuple with the number of failures and the number of tries.
  """
  finder = doctest.DocTestFinder(exclude_empty=False)
  runner = doctest.DocTestRunner(verbose=False)
  cov = coverage.coverage(source=[module.__name__])
  cov.erase()
  for test in finder.find(module, module.__name__):
    #print "Test: ", test.name
    cov.start()
    runner.run(test, out=lambda x: True)
    cov.stop()
  fn, allLines, notRun, fmtNotRun = cov.analysis(module)
  print "all: %d, not run: %d" % (len(allLines), len(notRun))
  print allLines
  print notRun

  cov.annotate(directory='.cov')
  return (runner.failures, runner.tries)


def testmod(module):
  """
  Mutation test all of a module's functions.
  """
  fails = runAllTestsCov(module)[0]
  if fails > 0: return (0, 0)

  mutations = [ComparisonMutation(),ModifyConstantMutation(),JumpMutation()]

  fails = 0
  attempts = 0

  for (name, function) in inspect.getmembers(module, inspect.isfunction):
    print "Testing %s" % name
    for mutation in mutations:
      f, a = mutation.runTests(module, function)

      fails += f
      attempts += a
    print

  return fails, attempts

if __name__ == '__main__':
  module = __import__(sys.argv[1])
  (fails, attempts) = testmod(module)
  if attempts == 0:
    print "Error: tests failed without mutation"
  else:
    print "Mutants: %d, Not Detected: %d, Score: %f%%" % (attempts, fails, 100.0 - fails * 100.0 / attempts)

__author__ = "Michael Stephens <me@mikej.st>"
__copyright__ = "Copyright (c) 2010 Michael Stephens"
__license__ = "BSD"
__version__ = "0.1"

