# source: http://danishmujeeb.com/blog/2014/01/basic-sorting-algorithms-implemented-in-python
import typ

import random

@typ.typ(items=[int])
def bubble_sort(items):
  """
  >>> bubble_sort([])
  []
  >>> bubble_sort([1])
  [1]
  >>> bubble_sort([2,1])
  [1, 2]
  >>> bubble_sort([1,2])
  [1, 2]
  >>> bubble_sort([1,2,2])
  [1, 2, 2]
  """
  for i in range(len(items)):
    for j in range(len(items)-1-i):
      if items[j] > items[j+1]:
        items[j], items[j+1] = items[j+1], items[j]   # Swap!
  return items

@typ.typ(items=[int])
def insertion_sort(items):
  """
  >>> insertion_sort([])
  []
  >>> insertion_sort([1])
  [1]
  >>> insertion_sort([2,1])
  [1, 2]
  >>> insertion_sort([1,2])
  [1, 2]
  >>> insertion_sort([1,2,2])
  [1, 2, 2]
  """
  for i in range(1, len(items)):
    j = i
    while j > 0 and items[j] < items[j-1]:
      items[j], items[j-1] = items[j-1], items[j]
      j -= 1
  return items

@typ.typ(items=[int])
def merge_sort(items):
  """
  >>> merge_sort([])
  []
  >>> merge_sort([1])
  [1]
  >>> merge_sort([2,1])
  [1, 2]
  >>> merge_sort([1,2])
  [1, 2]
  >>> merge_sort([1,2,2])
  [1, 2, 2]
  """
  if len(items) > 1:

    mid = len(items) / 2    # Determine the midpoint and split
    left = items[0:mid]
    right = items[mid:]

    merge_sort(left)      # Sort left list in-place
    merge_sort(right)       # Sort right list in-place

    l, r = 0, 0
    for i in range(len(items)):   # Merging the left and right list

      lval = left[l] if l < len(left) else None
      rval = right[r] if r < len(right) else None

      if (lval and rval and lval < rval) or rval is None:
        items[i] = lval
        l += 1
      elif (lval and rval and lval >= rval) or lval is None:
        items[i] = rval
        r += 1
      else:
        raise Exception('Could not merge, sub arrays sizes do not match the main array')
  return items

@typ.typ(items=[int])
def quick_sort(items):
  """
  >>> quick_sort([])
  []
  >>> quick_sort([1])
  [1]
  >>> quick_sort([2,1])
  [1, 2]
  >>> quick_sort([1,2])
  [1, 2]
  >>> quick_sort([1,2,2])
  [1, 2, 2]
  """
  if len(items) > 1:
    pivot_index = len(items) / 2
    smaller_items = []
    larger_items = []

    for i, val in enumerate(items):
      if i != pivot_index:
        if val < items[pivot_index]:
          smaller_items.append(val)
        else:
          larger_items.append(val)

    quick_sort(smaller_items)
    quick_sort(larger_items)
    items[:] = smaller_items + [items[pivot_index]] + larger_items
  return items


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

