import typ

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
 
