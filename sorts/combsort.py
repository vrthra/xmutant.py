import typ

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
 
