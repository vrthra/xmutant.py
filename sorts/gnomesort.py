import typ

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
 
