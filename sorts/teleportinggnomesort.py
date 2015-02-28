import typ

@typ.typ(items=[int])
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

