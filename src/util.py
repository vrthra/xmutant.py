import multiprocessing
import config
import sys
import os
import time
from logger import out
from itertools import izip

def spawn(f,arr):
  def fun(i,x):
    out().debug("spawn[%s] for input %s" % (os.getpid(), i))
    arr[i] = 0
    arr[i] = f(x)
  return fun

def parmap(f,X):
  arr = multiprocessing.Array('i', range(len(X)))
  proc=[(multiprocessing.Process(target=spawn(f,arr),args=(i,x)),x,i,arr) for (x,i) in izip(X,xrange(len(X)))]

  [p.start() for (p,x,i,a) in proc]

  alive = proc
  waitForMe = config.t['WaitSingleMutant']
  while waitForMe > 0 and len(alive) > 0:
    sys.stdout.flush()
    alive = [p for p in proc if p[0].is_alive()]
    waitForMe -= 1
    time.sleep(1)

  for (p,x,i,a) in alive:
    p.terminate()

  [p.join() for (p,i,x,a) in proc]
  return arr
