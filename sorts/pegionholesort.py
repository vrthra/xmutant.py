import typ

@typ.typ(items=[int])
def pigeonhole_sort(items):
  """
  >>> pigeonhole_sort([])
  []
  >>> pigeonhole_sort([1])
  [1]
  >>> pigeonhole_sort([2,1])
  [1, 2]
  >>> pigeonhole_sort([1,2])
  [1, 2]
  >>> pigeonhole_sort([1,2,2])
  [1, 2, 2]
  """
  if items == []: return items
  # size of range of values in the list (ie, number of pigeonholes we need)
  my_min = min(items)
  my_max = max(items)
  size = my_max - my_min + 1
 
  # our list of pigeonholes
  holes = [0] * size
 
  # Populate the pigeonholes.
  for x in items:
    holes[x - my_min] += 1
 
  # Put the elements back into the array in order.
  i = 0
  for count in range(size):
    while holes[count] > 0:
      holes[count] -= 1
      items[i] = count + my_min
      i += 1
  return items

