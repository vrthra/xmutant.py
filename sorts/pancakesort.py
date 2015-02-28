import typ

@typ.typ(items=[int])
def pancake_sort(items):
  """
  >>> pancake_sort([])
  []
  >>> pancake_sort([1])
  [1]
  >>> pancake_sort([2,1])
  [1, 2]
  >>> pancake_sort([1,2])
  [1, 2]
  >>> pancake_sort([1,2,2])
  [1, 2, 2]
  """
  if len(items) <= 1:
    return items
  for size in range(len(items), 1, -1):
    maxindex = max(range(size), key=items.__getitem__)
    if maxindex+1 != size:
      # This indexed max needs moving
      if maxindex != 0:
        # Flip the max item to the left
        items[:maxindex+1] = reversed(items[:maxindex+1])
      # Flip it into its final position
      items[:size] = reversed(items[:size])
  return items

