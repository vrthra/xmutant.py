import typ

@typ.skipit()
def _tree_insert(tree, element):
    if tree[0] > element:
        if not tree[1]:
            tree[1] = [element, [], []]
        else:
            tree[1] = _tree_insert(tree[1], element)
    else:
        if not tree[2]:
            tree[2] = [element, [], []]
        else:
            tree[2] = _tree_insert(tree[2], element)

    return tree


@typ.typ(items=[int])
def _tree_build(items):
    tree = [items[0], [], []]
    for element in items[1:]:
        tree = _tree_insert(tree, element)

    return tree

@typ.skipit()
def _tree_inorder(tree):
    # NOTE: returns work in a generator?
    if not tree:
        return

    for el in _tree_inorder(tree[1]):
        yield el

    yield tree[0]

    for el in _tree_inorder(tree[2]):
        yield el


@typ.typ(items=[int])
def tree_sort(items):
  """
  >>> tree_sort([])
  []
  >>> tree_sort([1])
  [1]
  >>> tree_sort([2,1])
  [1, 2]
  >>> tree_sort([1,2])
  [1, 2]
  >>> tree_sort([1,2,2])
  [1, 2, 2]
  """
  '''Tree sort is a sort algorithm that builds a binary search tree from
  the keys to be sorted, and then traverses the tree (in-order) so that the
  keys come out in sorted order. The algorithm can have O(n logn) running
  time if the binary tree is balanced.

  Running time: O(n^2).
  '''
  if items == []: return []
  reverse=False
  items = _tree_build(items)
  items = list(_tree_inorder(items))
  return items[::-1] if reverse else items
