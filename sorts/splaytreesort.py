import typ
import time
# not the splaysort. This is just a naive sort using a splay tree.
@typ.skipit()
class Node(object):
  """Nodes in the splay tree."""

  @typ.skipit()
  def __init__(self, key, value):
    self.key = key
    self.value = value
    self.left = None
    self.right = None


@typ.skipit()
class KeyNotFoundError(Exception):
  """KeyNotFoundError is raised when removing a non-existing node."""

  @typ.skipit()
  def __init__(self, key):
    self.key = key


@typ.skipit()
class SplayTree(object):
  """The splay tree itself is just a reference to the root of the tree."""

  @typ.skipit()
  def __init__(self):
    """Create a new SplayTree."""
    self.root = None

  @typ.skipit()
  def IsEmpty(self):
    """Is the SplayTree empty?"""
    return not self.root

  @typ.skipit()
  def Insert(self, key, value):
    """Insert a new node in the SplayTree."""
    # If the tree is empty, insert the new node.
    if self.IsEmpty():
      self.root = Node(key, value)
      return
    # Splay on the key to move the last node on the search path for
    # the key to the root of the tree.
    self.Splay(key)
    # Ignore repeated insertions with the same key.
    if self.root.key == key:
      self.root.value += 1
      return
    # Insert the new node.
    node = Node(key, value)
    if key > self.root.key:
      node.left = self.root
      node.right = self.root.right
      self.root.right = None
    else:
      node.right = self.root
      node.left = self.root.left
      self.root.left = None
    self.root = node

  @typ.skipit()
  def Remove(self, key):
    """Remove the node with the given key from the SplayTree."""
    # Raise exception for key that is not found if the tree is empty.
    if self.IsEmpty():
      raise KeyNotFoundError(key)
    # Splay on the key to move the node with the given key to the top.
    self.Splay(key)
    # Raise exception for key that is not found.
    if self.root.key != key:
      raise KeyNotFoundError(key)
    removed = self.root
    # Link out the root node.
    if not self.root.left:
      # No left child, so the new tree is just the right child.
      self.root = self.root.right
    else:
      # Left child exists.
      right = self.root.right
      # Make the original left child the new root.
      self.root = self.root.left
      # Splay to make sure that the new root has an empty right child.
      self.Splay(key)
      # Insert the original right child as the right child of the new
      # root.
      self.root.right = right
    return removed

  @typ.skipit()
  def Find(self, key):
    """Returns the node with the given key or None if no such node exists."""
    if self.IsEmpty():
      return None
    self.Splay(key)
    if self.root.key == key:
      return self.root
    return None

  @typ.skipit()
  def FindMax(self):
    """Returns the node with the largest key value."""
    if self.IsEmpty():
      return None
    current = self.root
    while current.right != None:
      current = current.right
    return current

  # Returns the node with the smallest key value.
  @typ.skipit()
  def FindMin(self):
    if self.IsEmpty():
      return None
    current = self.root
    while current.left != None:
      current = current.left
    return current

  @typ.skipit()
  def FindGreatestsLessThan(self, key):
    """Returns node with greatest key less than or equal to the given key."""
    if self.IsEmpty():
      return None
    # Splay on the key to move the node with the given key or the last
    # node on the search path to the top of the tree.
    self.Splay(key)
    # Now the result is either the root node or the greatest node in
    # the left subtree.
    if self.root.key <= key:
      return self.root
    else:
      tmp = self.root
      self.root = self.root.left
      result = self.FindMax()
      self.root = tmp
      return result

  @typ.skipit()
  def ExportKeyList(self):
    """Returns a list containing all the values of the nodes in the tree."""
    result = []
    nodes_to_visit = [self.root]
    while len(nodes_to_visit) > 0:
      node = nodes_to_visit.pop()
      if not node:
        continue
      for i in range(node.value + 1):
        result.append(node.key)
      nodes_to_visit.append(node.left)
      nodes_to_visit.append(node.right)
    return result

  @typ.skipit()
  def ExportValueList(self):
    """Returns a list containing all the values of the nodes in the tree."""
    result = []
    nodes_to_visit = [self.root]
    while len(nodes_to_visit) > 0:
      node = nodes_to_visit.pop()
      if not node:
        continue
      result.append(node.value)
      nodes_to_visit.append(node.left)
      nodes_to_visit.append(node.right)
    return result

  @typ.skipit()
  def Splay(self, key):
    """Perform splay operation.

    Perform the splay operation for the given key. Moves the node with
    the given key to the top of the tree.  If no node has the given
    key, the last node on the search path is moved to the top of the
    tree.

    This uses the simplified top-down splaying algorithm from:

    "Self-adjusting Binary Search Trees" by Sleator and Tarjan

    """
    if self.IsEmpty():
      return
    # Create a dummy node.  The use of the dummy node is a bit
    # counter-intuitive: The right child of the dummy node will hold
    # the L tree of the algorithm.  The left child of the dummy node
    # will hold the R tree of the algorithm.  Using a dummy node, left
    # and right will always be nodes and we avoid special cases.
    dummy = left = right = Node(None, None)
    current = self.root
    while True:
      if key < current.key:
        if not current.left:
          break
        if key < current.left.key:
          # Rotate right.
          tmp = current.left
          current.left = tmp.right
          tmp.right = current
          current = tmp
          if not current.left:
            break
        # Link right.
        right.left = current
        right = current
        current = current.left
      elif key > current.key:
        if not current.right:
          break
        if key > current.right.key:
          # Rotate left.
          tmp = current.right
          current.right = tmp.left
          tmp.left = current
          current = tmp
          if not current.right:
            break
        # Link left.
        left.right = current
        left = current
        current = current.right
      else:
        break
    # Assemble.
    left.right = current.left
    right.left = current.right
    current.left = dummy.right
    current.right = dummy.left
    self.root = current

@typ.typ(items=[int])
def splaytree_sort(items):
  """
  >>> splaytree_sort([])
  []
  >>> splaytree_sort([1])
  [1]
  >>> splaytree_sort([2,1])
  [1, 2]
  >>> splaytree_sort([1,2])
  [1, 2]
  >>> splaytree_sort([1,3,2])
  [1, 2, 3]
  >>> splaytree_sort([1,2,2])
  [1, 2, 2]
  """
  ret = []
  t = SplayTree()
  for i in items:
    t.Insert(i,0)
  while not(t.IsEmpty()):
    v = t.FindMin()
    t.Remove(v.key)
    for i in range(v.value + 1):
      ret.append(v.key)
  return ret

