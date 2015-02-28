import typ

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

