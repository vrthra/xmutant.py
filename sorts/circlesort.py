import typ

@typ.typ(items=[int], ln=int, rn=int)
def circle_sort_backend(items, ln, rn):
    n = rn-ln
    if n < 2:
        return 0
    swaps = 0
    m = n//2
    for i in range(m):
        if items[rn-(i+1)] < items[ln+i]:
            (items[rn-(i+1)], items[ln+i],) = (items[ln+i], items[rn-(i+1)],)
            swaps += 1
    if (n & 1) and (items[ln+m] < items[ln+m-1]):
        (items[ln+m-1], items[ln+m],) = (items[ln+m], items[ln+m-1],)
        swaps += 1
    return swaps + circle_sort_backend(items, ln, ln+m) + circle_sort_backend(items, ln+m, rn)
 

@typ.typ(items=[int])
def circle_sort(items):
  """
  >>> circle_sort([])
  []
  >>> circle_sort([1])
  [1]
  >>> circle_sort([2,1])
  [1, 2]
  >>> circle_sort([1,2])
  [1, 2]
  >>> circle_sort([1,2,2])
  [1, 2, 2]
  """
  s = 1
  while s: s = circle_sort_backend(items, 0, len(items))
  return items
 
