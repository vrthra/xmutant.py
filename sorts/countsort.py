import typ

@typ.typ(items=[int])
def count_sort(items):
  """
  >>> count_sort([])
  []
  >>> count_sort([1])
  [1]
  >>> count_sort([2,1])
  [1, 2]
  >>> count_sort([1,2])
  [1, 2]
  >>> count_sort([1,2,2])
  [1, 2, 2]
  """
  if items == []:
    return []
  counts = {}
  for num in items:
    if num in counts:
      counts[num] += 1
    else:
      counts[num] = 1

  sorted_list = []
  for num in xrange(min(items), max(items) + 1):
    if num in counts:
      for j in xrange(counts[num]):
        sorted_list.append(num)

  return sorted_list

