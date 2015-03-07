# source: http://danishmujeeb.com/blog/2014/01/basic-sorting-algorithms-implemented-in-python
import typ

@typ.skipit()
def columns(l):
  return [filter(None, x) for x in zip_longest(*l)]
try:
    from itertools import izip_longest as zip_longest
except:
    zip_longest = lambda *args: map(None, *args)

@typ.typ(items=[int])
def bead_sort(items):
  """
  >>> bead_sort([])
  []
  >>> bead_sort([1])
  [1]
  >>> bead_sort([2,1])
  [1, 2]
  >>> bead_sort([1,2])
  [1, 2]
  >>> bead_sort([1,2,2])
  [1, 2, 2]
  """
  x = columns([[1] * e for e in items])
  return list(reversed(map(len, columns(x))))

