#   http://www.iti.fh-flensburg.de/lang/algorithmen/sortieren/bitonic/oddn.htm
import typ

@typ.typ(items=[int], direction=bool)
def _merge(items, direction):
    if len(items) <= 1:
        return items

    #middle = 2 ** (int(log2(len(items))) - 1)
    middle = len(items) // 2
    items = _compare(items, middle, direction)

    first = _merge(items[:middle], direction)
    second = _merge(items[middle:], direction)

    return first + second


@typ.typ(items=[int], middle=int, direction=bool)
def _compare(items, middle, direction):
    for i in range(middle):
        if direction == (items[i] > items[i + middle]):
            items[i], items[i + middle] = items[i + middle], items[i]

    return items


@typ.typ(items=[int], direction=bool)
def _recsort(items, direction):
    if len(items) <= 1:
        return items

    #middle = 2 ** (int(log2(len(items))) - 1)
    middle = len(items) // 2
    first = _recsort(items[:middle], direction)
    second = _recsort(items[middle:], not direction)

    return _merge(first + second, direction)


@typ.typ(items=[int])
def bitonic_sort(items):
  """
  >>> bitonic_sort([])
  []
  >>> bitonic_sort([1])
  [1]
  >>> bitonic_sort([2,1])
  [1, 2]
  >>> bitonic_sort([1,2])
  [1, 2]
  >>> bitonic_sort([1,2,2])
  [1, 2, 2]
  """
  '''Bitonic Mergesort is a parallel sorting algorithm.

  The name comes from the idea of a `bitonic sequence`: a monotonic sequence
  is a sorted sequence (increasing or decreasing), a bitonic sequence is a
  sequence where:
  x_0 <= x_1 <= ... <= x_k >= x_{k + 1} ... >= x_n

  The algorithm is very similar to the classic Mergesort, as in: it splits
  the items in half, sorts one half increasingly and the second half
  decreasingly and then merges them.

  Running time: O(n log^2(n)).
  '''
  reverse=False
  if len(items) <= 1:
      return items

  items = _recsort(items, not reverse)
  return items
