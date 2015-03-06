import typ

@typ.typ(items=[int], x=int)
def binary_search(items, x):
  lo = 0
  hi = len(items)
  items.sort()
  while lo < hi:
    mid = (lo+hi)//2
    midval = items[mid]
    if midval < x:
      lo = mid+1
    elif midval > x: 
      hi = mid
    else:
      return mid
  return -1
