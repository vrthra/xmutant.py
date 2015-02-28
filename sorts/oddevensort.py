import typ

@typ.typ(items=[int])
def oddeven_sort(items):
  """
  >>> oddeven_sort([])
  []
  >>> oddeven_sort([1])
  [1]
  >>> oddeven_sort([2,1])
  [1, 2]
  >>> oddeven_sort([1,2])
  [1, 2]
  >>> oddeven_sort([1,2,2])
  [1, 2, 2]
  """
  '''Odd-Even Sort is a simple sorting algorithm based on Bubble Sort.

  It works by comparing all odd / even indexed adjacent pairs and swapping
  them if necessary.

  Running time: O(n ** 2).
  '''
  if len(items) <= 1:
      return items
  key=lambda x: x
  reverse=False
  swapped = True
  while swapped:
      swapped = False
      for i in range(1, len(items), 2):
          if key(items[i - 1]) > key(items[i]):
              items[i], items[i - 1] = items[i - 1], items[i]
              swapped = True

      for i in range(2, len(items), 2):
          if key(items[i - 1]) > key(items[i]):
              items[i], items[i - 1] = items[i - 1], items[i]
              swapped = True

  return items[::-1] if reverse else items
