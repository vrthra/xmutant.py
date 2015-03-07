import typ
import Queue as Q

@typ.skipit()
class Node(object):
  @typ.skipit()
  def __init__(self, parent, value, left, right):
    self.parent, self.value, self.left, self.right = parent, value, left, right

  @typ.skipit()
  def __cmp__(self, other):
    return cmp(self.value, other.value)


@typ.typ(items=[int])
def cartesiantree_sort(items):
  """
  >>> cartesiantree_sort([])
  []
  >>> cartesiantree_sort([1])
  [1]
  >>> cartesiantree_sort([2,1])
  [1, 2]
  >>> cartesiantree_sort([1,2])
  [1, 2]
  >>> cartesiantree_sort([1,2,2])
  [1, 2, 2]
  """
  queue = q = Q.PriorityQueue()
  
  length = len(items)
  if length <= 1: return items
  
  root = Node(None, items[0], None, None)
  last = root
  
  for i in xrange(1, length):
    while last and last.value > items[i]:
      last = last.parent
    if last:
      last.right = Node(last, items[i], last.right, None)
      last = last.right
    else:
      root = Node(None, items[i], root, None)
      last = root
  queue.put(root)
  items = []
  while not(queue.empty()):
    node = queue.get()
    items.append(node.value)
    
    if node.left:
      queue.put(node.left)
    if node.right:
      queue.put(node.right)
  return items

