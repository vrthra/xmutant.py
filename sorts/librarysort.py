import typ

@typ.typ(items=[int])
def library_sort(items):
  """
  >>> library_sort([])
  []
  >>> library_sort([1])
  [1]
  >>> library_sort([2,1])
  [1, 2]
  >>> library_sort([1,2])
  [1, 2]
  >>> library_sort([1,2,2])
  [1, 2, 2]
  """
  '''Library sort, or gapped insertion sort is a sorting algorithm that
  uses an insertion sort, but with gaps in the items to accelerate
  subsequent insertions.

  As the name aptly suggests, the sorting algorithm creates an items with
  gaps between the elements and then at the end it just picks the ones that
  were filled. In more detail:
  * construct an expanded items of (1 + factor) times the length of the
  original items
  * at each step add 2 ** i elements into the expanded items, this maintains
  a sorted order of the expanded items.
  * move the inserted elements around so that we still have gaps to insert
  into.

  Running time: worst case O(n^2), average case O(n logn).
  '''
  if items == []: return []
  key = lambda x: x
  reverse=False
  factor = 0.7
  length = len(items)
  elength = int((1 + factor) * length)

  ordered_array = [None] * elength

  index = 1
  numi = 1
  ordered_array[0] = items[0]

  while length > numi:
      for i in range(numi):
          low = 0
          high = 2 * numi - 1

          while low <= high:
              mid = (low + high) // 2
              saved_mid = mid

              while mid < elength and ordered_array[mid] is None:
                  if mid == high:
                      mid = saved_mid - 1
                      while mid > 0 and ordered_array[mid] is None:
                          mid -= 1
                      break
                  mid += 1

              if items[index] > ordered_array[mid]:
                  low = mid + 1
                  while low < elength and ordered_array[low] is None:
                      low += 1
              else:
                  high = mid - 1

          if ordered_array[high + 1] is None:
              ordered_array[high + 1] = items[index]
          else:
              temp = high + 1
              while ordered_array[temp] is not None:
                  temp -= 1
                  if temp < 0:
                      temp = high + 1
                      break

              while temp < elength and ordered_array[temp] is not None:
                  temp += 1

              while temp < high:
                  ordered_array[temp] = ordered_array[temp + 1]
                  temp += 1

              while temp > (high + 1):
                  ordered_array[temp] = ordered_array[temp - 1]
                  temp -= 1

              ordered_array[temp] = items[index]

          index += 1
          if index == length:
              break

      numi *= 2
      for i in range(numi, 0, -1):
          if ordered_array[i] is None:
              continue

          generated_index = i * 2
          if generated_index >= elength:
              generated_index = elength - 1
              if ordered_array[generated_index] is not None:
                  break
          ordered_array[generated_index] = ordered_array[i]
          ordered_array[i] = None

  items = [x for x in ordered_array if x is not None]
  return items[::-1] if reverse else items
