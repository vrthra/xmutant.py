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
def selection_sort(items):
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
  for i in range(0,len(items)-1):
    mn = min(range(i,len(items)), key=items.__getitem__)
    items[i],items[mn] = items[mn],items[i]
  return items

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

@typ.typ(items=[int])
def count_sort(items):
  """
  >>> count_sort([])
  []
  >>> count_sort([1])
  [1]
  >>> count_sort([2,1])
  [1, 2]
  >>> count_sort([1,2])
  [1, 2]
  >>> count_sort([1,2,2])
  [1, 2, 2]
  """
  if items == []:
    return []
  counts = {}
  for num in items:
    if num in counts:
      counts[num] += 1
    else:
      counts[num] = 1

  sorted_list = []
  for num in range(min(items), max(items) + 1):
    if num in counts:
      for j in range(counts[num]):
        sorted_list.append(num)

  return sorted_list

@typ.typ(items=[int])
def pancake_sort(items):
  """
  >>> pancake_sort([])
  []
  >>> pancake_sort([1])
  [1]
  >>> pancake_sort([2,1])
  [1, 2]
  >>> pancake_sort([1,2])
  [1, 2]
  >>> pancake_sort([1,2,2])
  [1, 2, 2]
  """
  if len(items) <= 1:
    return items
  for size in range(len(items), 1, -1):
    maxindex = max(range(size), key=items.__getitem__)
    if maxindex+1 != size:
      # This indexed max needs moving
      if maxindex != 0:
        # Flip the max item to the left
        items[:maxindex+1] = reversed(items[:maxindex+1])
      # Flip it into its final position
      items[:size] = reversed(items[:size])
  return items

@typ.typ(items=[int])
def pigeonhole_sort(items):
  """
  >>> pigeonhole_sort([])
  []
  >>> pigeonhole_sort([1])
  [1]
  >>> pigeonhole_sort([2,1])
  [1, 2]
  >>> pigeonhole_sort([1,2])
  [1, 2]
  >>> pigeonhole_sort([1,2,2])
  [1, 2, 2]
  """
  if items == []: return items
  # size of range of values in the list (ie, number of pigeonholes we need)
  my_min = min(items)
  my_max = max(items)
  size = my_max - my_min + 1
 
  # our list of pigeonholes
  holes = [0] * size
 
  # Populate the pigeonholes.
  for x in items:
    holes[x - my_min] += 1
 
  # Put the elements back into the array in order.
  i = 0
  for count in range(size):
    while holes[count] > 0:
      holes[count] -= 1
      items[i] = count + my_min
      i += 1
  return items


@typ.typ(items=[int])
def bucket_sort(items):
  """
  >>> bucket_sort([])
  []
  >>> bucket_sort([1])
  [1]
  >>> bucket_sort([2,1])
  [1, 2]
  >>> bucket_sort([1,2])
  [1, 2]
  >>> bucket_sort([1,2,2])
  [1, 2, 2]
  """
  buckets = {}
  m = 100 # buckets
  n = len(items)
  for j in range(m):
    buckets[j] = 0
  for i in range(n):
    buckets[items[i]] += 1
  i = 0
  for j in range(m):
    for k in range(buckets[j]):
      items[i] = j
      i += 1
  return items

@typ.typ(items=[int])
def cocktail_sort(items):
  """
  >>> cocktail_sort([])
  []
  >>> cocktail_sort([1])
  [1]
  >>> cocktail_sort([2,1])
  [1, 2]
  >>> cocktail_sort([1,2])
  [1, 2]
  >>> cocktail_sort([1,2,2])
  [1, 2, 2]
  """
  for k in range(len(items)-1, 0, -1):
    swapped = False
    for i in range(k, 0, -1):
      if items[i]<items[i-1]:
        items[i], items[i-1] = items[i-1], items[i]
        swapped = True
 
    for i in range(k):
      if items[i] > items[i+1]:
        items[i], items[i+1] = items[i+1], items[i]
        swapped = True
 
    if not swapped:
      return items
  return items


@typ.typ(items=[int])
def counting_sort(items):
  """
  >>> counting_sort([])
  []
  >>> counting_sort([1])
  [1]
  >>> counting_sort([2,1])
  [1, 2]
  >>> counting_sort([1,2])
  [1, 2]
  >>> counting_sort([1,2,2])
  [1, 2, 2]
  """
  """in-place counting sort"""
  maxval = 10000
  m = maxval + 1
  count = [0] * m         # init with zeros
  for a in items:
    count[a] += 1       # count occurences
  i = 0
  for a in range(m):      # emit
    for c in range(count[a]): # - emit 'count[a]' copies of 'a'
      items[i] = a
      i += 1
  return items

@typ.typ(items=[int])
def gnome_sort(items):
  """
  >>> gnome_sort([])
  []
  >>> gnome_sort([1])
  [1]
  >>> gnome_sort([2,1])
  [1, 2]
  >>> gnome_sort([1,2])
  [1, 2]
  >>> gnome_sort([1,2,2])
  [1, 2, 2]
  """
  i = 0
  n = len(items)
  while i < n:
    if i and items[i] < items[i-1]:
      items[i], items[i-1] = items[i-1], items[i]
      i -= 1
    else:
      i += 1
  return items
 
def teleportinggnome_sort(items):
  """
  >>> teleportinggnome_sort([])
  []
  >>> teleportinggnome_sort([1])
  [1]
  >>> teleportinggnome_sort([2,1])
  [1, 2]
  >>> teleportinggnome_sort([1,2])
  [1, 2]
  >>> teleportinggnome_sort([1,2,2])
  [1, 2, 2]
  """
  i = j = 0
  n = len(items)
  while i < n:
    if i and items[i] < items[i-1]:
      items[i], items[i-1] = items[i-1], items[i]
      i -= 1
    else:
      if i < j: # teleport!
        i = j
      j = i = i+1
  return items


import bisect, heapq
 
@typ.typ(items=[int])
def patience_sort(items):
  """
  >>> patience_sort([])
  []
  >>> patience_sort([1])
  [1]
  >>> patience_sort([2,1])
  [1, 2]
  >>> patience_sort([1,2])
  [1, 2]
  >>> patience_sort([1,2,2])
  [1, 2, 2]
  """
  piles = []
  for x in items:
    new_pile = [x]
    i = bisect.bisect_left(piles, new_pile)
    if i != len(piles):
      piles[i].insert(0, x)
    else:
      piles.append(new_pile)
  # priority queue allows us to retrieve least pile efficiently
  for i in range(len(items)):
    small_pile = piles[0]
    items[i] = small_pile.pop(0)
    if small_pile:
      heapq.heapreplace(piles, small_pile)
    else:
      heapq.heappop(piles)
  return items 

 
@typ.typ(items=[int])
def strand_sort(items):
  """
  >>> strand_sort([])
  []
  >>> strand_sort([1])
  [1]
  >>> strand_sort([2,1])
  [1, 2]
  >>> strand_sort([1,2])
  [1, 2]
  >>> strand_sort([1,2,2])
  [1, 2, 2]
  """
  nitems = len(items)
  sortedBins = []
  while( len(items) > 0 ):
      highest = float("-inf")
      newBin = []
      i = 0
      while( i < len(items) ):
          if( items[i] >= highest ):
              highest = items.pop(i)
              newBin.append( highest )
          else:
              i=i+1
      sortedBins.append(newBin)
   
  sorted = []
  while( len(sorted) < nitems ):
      lowBin = 0
      for j in range( 0, len(sortedBins) ):
          if( sortedBins[j][0] < sortedBins[lowBin][0] ):
              lowBin = j
      sorted.append( sortedBins[lowBin].pop(0) )
      if( len(sortedBins[lowBin]) == 0 ):
          del sortedBins[lowBin]
  return sorted
   
# @typ.typ(items=[int])
# def cycle_sort(items):
#   """
#   >>> cycle_sort([])
#   []
#   >>> cycle_sort([1])
#   [1]
#   >>> cycle_sort([2,1])
#   [1, 2]
#   >>> cycle_sort([1,2])
#   [1, 2]
#   >>> cycle_sort([1,2,2])
#   [1, 2, 2]
#   """
#   for i in range(len(items)):
#     if i != items[i]:
#       n = i
#       while 1: 
#         tmp = items[int(n)]
#         if n != i:
#           items[int(n)] = last_value
#         else:
#           items[int(n)] = None
#         last_value = tmp
#         n = last_value
#         if n == i:
#           items[int(n)] = last_value
#           break
#   return items

# def columns(l):
#   return [filter(None, x) for x in zip_longest(*l)]
# try:
#     from itertools import izip_longest as zip_longest
# except:
#     zip_longest = lambda *args: map(None, *args)
# 
# @typ.typ(items=[int])
# def bead_sort(items):
#   """
#   >>> bead_sort([])
#   []
#   >>> bead_sort([1])
#   [1]
#   >>> bead_sort([2,1])
#   [1, 2]
#   >>> bead_sort([1,2])
#   [1, 2]
#   >>> bead_sort([1,2,2])
#   [1, 2, 2]
#   """
#   x = columns([[1] * e for e in items])
#   return rev(map(len, columns(x)))
# 
