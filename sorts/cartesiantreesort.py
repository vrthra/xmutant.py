import typ

@typ.typ(heapList=[int], currentSize=[int])
class BinHeap:
  """
  >>> queue = BinHeap()
  >>> queue.put(9)
  >>> queue.put(5)
  >>> queue.put(6)
  >>> queue.put(2)
  >>> queue.put(3)
  >>> queue.get()
  2
  """
  @typ.typ(self='cartesiantreesort.BinHeap')
  def __init__(self):
    self.heapList = [0]
    self.currentSize = 0


  @typ.typ(self='cartesiantreesort.BinHeap', i=int)
  def percUp(self,i):
    while i // 2 > 0:
      if self.heapList[i] < self.heapList[i // 2]:
       tmp = self.heapList[i // 2]
       self.heapList[i // 2] = self.heapList[i]
       self.heapList[i] = tmp
      i = i // 2

  @typ.typ(self='cartesiantreesort.BinHeap', k=int)
  def put(self,k):
    self.heapList.append(k)
    self.currentSize = self.currentSize + 1
    self.percUp(self.currentSize)

  @typ.typ(self='cartesiantreesort.BinHeap', i=int)
  def percDown(self,i):
    while (i * 2) <= self.currentSize:
      mc = self.minChild(i)
      if self.heapList[i] > self.heapList[mc]:
        tmp = self.heapList[i]
        self.heapList[i] = self.heapList[mc]
        self.heapList[mc] = tmp
      i = mc

  @typ.typ(self='cartesiantreesort.BinHeap', i=int)
  def minChild(self,i):
    if i * 2 + 1 > self.currentSize:
      return i * 2
    else:
      if self.heapList[i*2] < self.heapList[i*2+1]:
        return i * 2
      else:
        return i * 2 + 1

  @typ.typ(self='cartesiantreesort.BinHeap')
  def get(self):
    retval = self.heapList[1]
    self.heapList[1] = self.heapList[self.currentSize]
    self.currentSize = self.currentSize - 1
    self.heapList.pop()
    self.percDown(1)
    return retval

  @typ.typ(self='cartesiantreesort.BinHeap')
  def empty(self):
    return self.currentSize == 0

  @typ.typ(self='cartesiantreesort.BinHeap', alist=[int])
  def buildHeap(self,alist):
    i = len(alist) // 2
    self.currentSize = len(alist)
    self.heapList = [0] + alist[:]
    while (i > 0):
      self.percDown(i)
      i = i - 1

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
  queue = BinHeap()
  
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

