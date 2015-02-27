import typ
@typ.typ(items=[int], t=int)
def binary_search(items, t):
  """
  >>> binary_search([0,1,2,3,4,5], 2)
  2
  >>> binary_search([0,1,2,3,4,5], 6)
  -1
  >>> binary_search([1,2,3,4,5], 3)
  2
  """
  min = 0
  max = len(items) - 1
  while True:
    if max < min:
      return -1
    m = (min + max) // 2
    if items[m] < t:
      min = m + 1
    elif items[m] > t:
      max = m - 1
    else:
      return m
