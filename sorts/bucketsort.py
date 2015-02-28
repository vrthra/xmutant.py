import typ

@typ.typ(items=[int])
def bucket_sort(items):
  """
  >>> bucket_sort([])
  []
  >>> bucket_sort([1])
  [1]
  >>> bucket_sort([2,1])
  [1, 2]
  >>> bucket_sort([1,2])
  [1, 2]
  >>> bucket_sort([1,2,2])
  [1, 2, 2]
  """
  buckets = {}
  m = 100 # buckets
  n = len(items)
  for j in range(m):
    buckets[j] = 0
  for i in range(n):
    buckets[items[i]] += 1
  i = 0
  for j in range(m):
    for k in range(buckets[j]):
      items[i] = j
      i += 1
  return items

