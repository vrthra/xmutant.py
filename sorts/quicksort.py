import typ

@typ.typ(items=[int])
def quick_sort(items):
  """
  >>> quick_sort([])
  []
  >>> quick_sort([1])
  [1]
  >>> quick_sort([2,1])
  [1, 2]
  >>> quick_sort([1,2])
  [1, 2]
  >>> quick_sort([1,2,2])
  [1, 2, 2]
  """
  if len(items) > 1:
    pivot_index = len(items) / 2
    smaller_items = []
    larger_items = []

    for i, val in enumerate(items):
      if i != pivot_index:
        if val < items[pivot_index]:
          smaller_items.append(val)
        else:
          larger_items.append(val)

    quick_sort(smaller_items)
    quick_sort(larger_items)
    items[:] = smaller_items + [items[pivot_index]] + larger_items
  return items

