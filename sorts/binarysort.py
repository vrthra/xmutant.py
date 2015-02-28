import typ

@typ.typ(items=[int])
def binary_sort(items):
  """
  >>> binary_sort([])
  []
  >>> binary_sort([1])
  [1]
  >>> binary_sort([2,1])
  [1, 2]
  >>> binary_sort([1,2])
  [1, 2]
  >>> binary_sort([1,2,2])
  [1, 2, 2]
  """
  initial_left = 0
  initial_right = len(items) - 1
  new_list = []
  if initial_right > initial_left:
    new_list.append(items[initial_left])
  for pivot in items[initial_left + 1:]:
    new_list_len_minus_1 = len(new_list) - 1

    left_for_binary_search = 0
    right_for_binary_search = new_list_len_minus_1

    assert left_for_binary_search <= right_for_binary_search

    while left_for_binary_search < right_for_binary_search:
      midpoint = (left_for_binary_search + right_for_binary_search) / 2
      if pivot < new_list[midpoint]:
        right_for_binary_search = midpoint
      else:
        left_for_binary_search = midpoint + 1

    assert left_for_binary_search == right_for_binary_search

    if new_list[left_for_binary_search] < pivot:
      # we are >=
      new_list.insert(left_for_binary_search + 1, pivot)
    else:
      # we are <, insert before
      new_list.insert(left_for_binary_search, pivot)

  # now copy to the original list
  for index, value in enumerate(new_list):
    items[initial_left + index] = value
  return items

