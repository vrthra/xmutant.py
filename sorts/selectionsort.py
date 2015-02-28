import typ

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

