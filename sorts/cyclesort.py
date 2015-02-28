import typ

@typ.typ(items=[int])
def cycle_sort(items):
  """
  >>> cycle_sort([])
  []
  >>> cycle_sort([1])
  [1]
  >>> cycle_sort([2,1])
  [1, 2]
  >>> cycle_sort([1,2])
  [1, 2]
  >>> cycle_sort([1,2,2])
  [1, 2, 2]
  """
  writes = 0
 
  # Loop through the items to find cycles to rotate.
  for cycleStart, item in enumerate(items):
 
    # Find where to put the item.
    pos = cycleStart
    for item2 in items[cycleStart + 1:]:
      if item2 < item:
        pos += 1
 
    # If the item is already there, this is not a cycle.
    if pos == cycleStart:
      continue
 
    # Otherwise, put the item there or right after any duplicates.
    while item == items[pos]:
      pos += 1
    items[pos], item = item, items[pos]
    writes += 1
 
    # Rotate the rest of the cycle.
    while pos != cycleStart:
 
      # Find where to put the item.
      pos = cycleStart
      for item2 in items[cycleStart + 1:]:
        if item2 < item:
          pos += 1
 
      # Put the item there or right after any duplicates.
      while item == items[pos]:
        pos += 1
      items[pos], item = item, items[pos]
      writes += 1
  return items

