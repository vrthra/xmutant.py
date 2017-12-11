import typ

# source: http://danishmujeeb.com/blog/2014/01/basic-sorting-algorithms-implemented-in-python
@typ.typ(items=[int])
def heap_sort(items):
  """
  >>> heap_sort([])
  []
  >>> heap_sort([1])
  [1]
  >>> heap_sort([2,1])
  [1, 2]
  >>> heap_sort([1,2])
  [1, 2]
  >>> heap_sort([1,2,2])
  [1, 2, 2]
  """
  # in pseudo-code, heapify only called once, so inline it here
  for start in range((len(items)-2)//2, -1, -1):
    siftdown(items, start, len(items)-1)
 
  for end in range(len(items)-1, 0, -1):
    items[end], items[0] = items[0], items[end]
    siftdown(items, 0, end - 1)
  return items
 
@typ.typ(items=[int], start=int, end=int)
def siftdown(items, start, end):
  root = start
  while True:
    child = root * 2 + 1
    if child > end: break
    if child + 1 <= end and items[child] < items[child + 1]:
      child += 1
    if items[root] < items[child]:
      items[root], items[child] = items[child], items[root]
      root = child
    else:
      break
