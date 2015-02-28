import typ
import math, copy

@typ.typ(x=int, digit=int, radix=int)
def get_radix_val(x, digit, radix):
    return int(math.floor(x / radix**digit)) % radix
 
@typ.typ(items=[int], start=int, end=int, digit=int, radix=int)
def compute_offsets(items, start, end, digit, radix):
    counts = [0 for _ in range(radix)]
    for i in range(start, end):
        val = get_radix_val(items[i], digit, radix)
        counts[val] += 1
    offsets = [0 for _ in range(radix)]
    sum = 0
    for i in range(radix):
        offsets[i] = sum
        sum += counts[i]
    return offsets
 
@typ.typ(items=[int], offsets=[int], start=int, end=int, digit=int, radix=int)
def swap(items, offsets, start, end, digit, radix):
    i = start
    next_free = copy.copy(offsets)
    cur_block = 0
    while cur_block < radix-1:
        if i >= offsets[cur_block+1]:
            cur_block += 1
            continue
        radix_val = get_radix_val(items[i], digit, radix)
        if radix_val == cur_block:
            i += 1
            continue
        swap_to = next_free[radix_val]
        items[i], items[swap_to] = items[swap_to], items[i]
        next_free[radix_val] += 1
 
@typ.typ(items=[int], start=int, end=int, digit=int, radix=int)
def flag_sort_helper(items, start, end, digit, radix):
    offsets = compute_offsets(items, start, end, digit, radix)
    swap(items, offsets, start, end, digit, radix)
    if digit == 0:
        return
    for i in range(len(offsets)-1):
        flag_sort_helper(items, offsets[i], offsets[i+1], digit-1, radix)

@typ.typ(items=[int])
def flag_sort(items):
  """
  >>> flag_sort([])
  []
  >>> flag_sort([1])
  [1]
  >>> flag_sort([2,1])
  [1, 2]
  >>> flag_sort([1,2])
  [1, 2]
  >>> flag_sort([1,2,2])
  [1, 2, 2]
  """
  if items == []: return []
  radix = 64
  for x in items:
      assert(type(x) == int)
  max_val = max(items)
  max_digit = int(math.floor(math.log(max_val, radix)))
  flag_sort_helper(items, 0, len(items), max_digit, radix)
  return items
