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

@typ.typ(items=[int])
def shell_sort(items):
  """
  >>> shell_sort([])
  []
  >>> shell_sort([1])
  [1]
  >>> shell_sort([2,1])
  [1, 2]
  >>> shell_sort([1,2])
  [1, 2]
  >>> shell_sort([1,2,2])
  [1, 2, 2]
  """
  inc = len(items) // 2
  while inc:
    for i, el in enumerate(items):
      while i >= inc and items[i - inc] > el:
        items[i] = items[i - inc]
        i -= inc
      items[i] = el
    inc = 1 if inc == 2 else int(inc * 5.0 / 11)
  return items
 
@typ.typ(items=[int])
def comb_sort(items):
  """
  >>> comb_sort([])
  []
  >>> comb_sort([1])
  [1]
  >>> comb_sort([2,1])
  [1, 2]
  >>> comb_sort([1,2])
  [1, 2]
  >>> comb_sort([1,2,2])
  [1, 2, 2]
  """
  gap = len(items)
  swaps = True
  while gap > 1 or swaps:
    gap = max(1, int(gap / 1.25))  # minimum gap is 1
    swaps = False
    for i in range(len(items) - gap):
      j = i+gap
      if items[i] > items[j]:
        items[i], items[j] = items[j], items[i]
        swaps = True
  return items
 
@typ.typ(items=[int])
def selection_sort(lst):
  """
  >>> selection_sort([])
  []
  >>> selection_sort([1])
  [1]
  >>> selection_sort([2,1])
  [1, 2]
  >>> selection_sort([1,2])
  [1, 2]
  >>> selection_sort([1,2,2])
  [1, 2, 2]
  """
  for i in range(0,len(lst)-1):
    mn = min(range(i,len(lst)), key=lst.__getitem__)
    lst[i],lst[mn] = lst[mn],lst[i]
  return lst

@typ.typ(items=[int])
def radix_sort(items):
  """
  >>> radix_sort([])
  []
  >>> radix_sort([1])
  [1]
  >>> radix_sort([2,1])
  [1, 2]
  >>> radix_sort([1,2])
  [1, 2]
  >>> radix_sort([1,2,2])
  [1, 2, 2]
  """
  radix = 10
  max_len = False
  tmp, placement = -1, 1
  while not max_len:
    max_len = True
    # declare and initialize buckets
    buckets = [list() for _ in range( radix )]
    # split items between lists
    for  i in items:
      tmp = i / placement
      buckets[tmp % radix].append( i )
      if max_len and tmp > 0:
        max_len = False
    # empty lists into items array
    a = 0
    for b in range( radix ):
      buck = buckets[b]
      for i in buck:
        items[a] = i
        a += 1
    # move to next digit
    placement *= radix
  return items

@typ.typ(items=[int])
def binary_sort(items):
  """
  >>> binary_sort([])
  []
  >>> binary_sort([1])
  [1]
  >>> binary_sort([2,1])
  [1, 2]
  >>> binary_sort([1,2])
  [1, 2]
  >>> binary_sort([1,2,2])
  [1, 2, 2]
  """
  initial_left = 0
  initial_right = len(items) - 1
  new_list = []
  if initial_right > initial_left:
    new_list.append(items[initial_left])
  for pivot in items[initial_left + 1:]:
    new_list_len_minus_1 = len(new_list) - 1

    left_for_binary_search = 0
    right_for_binary_search = new_list_len_minus_1

    assert left_for_binary_search <= right_for_binary_search

    while left_for_binary_search < right_for_binary_search:
      midpoint = (left_for_binary_search + right_for_binary_search) / 2
      if pivot < new_list[midpoint]:
        right_for_binary_search = midpoint
      else:
        left_for_binary_search = midpoint + 1

    assert left_for_binary_search == right_for_binary_search

    if new_list[left_for_binary_search] < pivot:
      # we are >=
      new_list.insert(left_for_binary_search + 1, pivot)
    else:
      # we are <, insert before
      new_list.insert(left_for_binary_search, pivot)

  # now copy to the original list
  for index, value in enumerate(new_list):
    items[initial_left + index] = value
  return items

