import multiprocessing
import config
import sys
import os
import time
from logger import out
from itertools import izip

class MPool(object):
  def __init__(self, procs):
    self.procs = procs
    self.rest = procs
    self.proc_registry = {}
    self.waitTime = config.t['WaitSingleMutant']
    for p in self.procs: self.proc_registry[p] = 0
    out().info("MPool with %s inputs" % len(procs))

  def spawn(self, nprocs):
    out().info("spawn: %s procs" % nprocs)
    now = self.rest[0:nprocs]
    self.rest = self.rest[nprocs:]
    for p in now:
      p.daemon = True
      p.start()
      self.proc_registry[p] = time.time()
    out().info("spawn: Spawned %s, %s pending" % (len(now), len(self.rest)))

  def more(self):
    out().debug("more: %s" % len(self.proc_registry.keys()))
    return len(self.proc_registry.keys()) > 0

  def wait(self, npool):
    out().info("wait: Pool capacity %s" % npool)
    vacancy = npool
    while True:
      if vacancy > 0: self.spawn(vacancy)
      vacancy = self.reap_dead()
      if self.more(): time.sleep(1)
      else: break

  def reap_dead(self):
    t = time.time()
    dead = 0
    for (p,ptime) in self.proc_registry.items():
      if ptime == 0: # not started yet.
        continue
      if p.is_alive():
        out().debug("reap_dead: alive %s (%s > %s)" % (p.name, t-ptime, self.waitTime))
        if (t - ptime) > self.waitTime:
          out().info("reap_dead: terminate %s" % p.name)
          p.terminate()
      if not(p.is_alive()):
        self.proc_registry.pop(p)
        dead += 1
    return dead


def fnwrap(f,arr):
  def fun(i,x):
    out().debug("fnwrap[%s] for input %s" % (os.getpid(), i))
    arr[i] = 0
    arr[i] = f(x)
  return fun

def parmap(f,X):
  arr = multiprocessing.Array('i', range(len(X)))
  procs=[multiprocessing.Process(target=fnwrap(f,arr),args=(i,x)) for (x,i) in izip(X,xrange(len(X)))]
  mp = MPool(procs)
  mp.wait(multiprocessing.cpu_count() - 1 or 1)
  return arr
