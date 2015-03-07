# source: http://danishmujeeb.com/blog/2014/01/basic-sorting-algorithms-implemented-in-python
import typ
from itertools import izip_longest as zip_longest

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
  y = [[1] * e for e in items]
  x = [filter(None, i) for i in zip_longest(*y)]
  z = [filter(None, i) for i in zip_longest(*x)]
  return list(reversed(map(len, z)))

