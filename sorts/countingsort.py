import typ

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

