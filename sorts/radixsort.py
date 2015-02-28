import typ

@typ.typ(items=[int])
def radix_sort(items):
  """
  >>> radix_sort([])
  []
  >>> radix_sort([1])
  [1]
  >>> radix_sort([2,1])
  [1, 2]
  >>> radix_sort([1,2])
  [1, 2]
  >>> radix_sort([1,2,2])
  [1, 2, 2]
  """
  radix = 10
  max_len = False
  tmp, placement = -1, 1
  while not max_len:
    max_len = True
    # declare and initialize buckets
    buckets = [list() for _ in range( radix )]
    # split items between lists
    for  i in items:
      tmp = i / placement
      buckets[tmp % radix].append( i )
      if max_len and tmp > 0:
        max_len = False
    # empty lists into items array
    a = 0
    for b in range( radix ):
      buck = buckets[b]
      for i in buck:
        items[a] = i
        a += 1
    # move to next digit
    placement *= radix
  return items

