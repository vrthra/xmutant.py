import math
import random
import typ

@typ.typ(items=[int])
def heap_sort(items):
  """
  >>> heap_sort([])
  []
  >>> heap_sort([1])
  [1]
  >>> heap_sort([2,1])
  [1, 2]
  >>> heap_sort([1,2])
  [1, 2]
  >>> heap_sort([1,2,2])
  [1, 2, 2]
  """
  # in pseudo-code, heapify only called once, so inline it here
  for start in range((len(items)-2)/2, -1, -1):
    siftdown(items, start, len(items)-1)
 
  for end in range(len(items)-1, 0, -1):
    items[end], items[0] = items[0], items[end]
    siftdown(items, 0, end - 1)
  return items
 
@typ.typ(items=[int], start=int, end=int)
def siftdown(items, start, end):
  root = start
  while True:
    child = root * 2 + 1
    if child > end: break
    if child + 1 <= end and items[child] < items[child + 1]:
      child += 1
    if items[root] < items[child]:
      items[root], items[child] = items[child], items[root]
      root = child
    else:
      break

@typ.typ(items=[int], depth=int)
def _depthsort(items, depth):
    if len(items) <= 1: return items

    if depth == 0: return heap_sort(items)

    pivot = random.randrange(len(items))
    e = items.pop(pivot)

    left = _depthsort([x for x in items if x < e], depth - 1)
    right = _depthsort([x for x in items if x >= e], depth - 1)

    return left + [e] + right

@typ.typ(items=[int])
def intro_sort(items):
  """
  >>> intro_sort([])
  []
  >>> intro_sort([1])
  [1]
  >>> intro_sort([2,1])
  [1, 2]
  >>> intro_sort([1,2])
  [1, 2]
  >>> intro_sort([1,2,2])
  [1, 2, 2]
  """
  '''Introsort is a sorting algorithm developed by David Musser in 1997.
  It uses Quicksort and Heapsort when convenient to get over Quicksort's
  worst-case scenario of O(n^2).

  It usually switches to Heapsort when the heap would be a nice logn.

  Running time: O(n logn).
  '''

  reverse = False
  if len(items) <= 1: return items

  items = _depthsort(items, int(math.log(len(items), 2)))
  return items[::-1] if reverse else items

