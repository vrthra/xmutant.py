import typ
import bisect, heapq
 
@typ.typ(items=[int])
def patience_sort(items):
  """
  >>> patience_sort([])
  []
  >>> patience_sort([1])
  [1]
  >>> patience_sort([2,1])
  [1, 2]
  >>> patience_sort([1,2])
  [1, 2]
  >>> patience_sort([1,2,2])
  [1, 2, 2]
  """
  piles = []
  for x in items:
    new_pile = [x]
    i = bisect.bisect_left(piles, new_pile)
    if i != len(piles):
      piles[i].insert(0, x)
    else:
      piles.append(new_pile)
  # priority queue allows us to retrieve least pile efficiently
  for i in xrange(len(items)):
    small_pile = piles[0]
    items[i] = small_pile.pop(0)
    if small_pile:
      heapq.heapreplace(piles, small_pile)
    else:
      heapq.heappop(piles)
  return items 

