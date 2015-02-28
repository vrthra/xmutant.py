import typ

@typ.typ(items=[int])
def cocktail_sort(items):
  """
  >>> cocktail_sort([])
  []
  >>> cocktail_sort([1])
  [1]
  >>> cocktail_sort([2,1])
  [1, 2]
  >>> cocktail_sort([1,2])
  [1, 2]
  >>> cocktail_sort([1,2,2])
  [1, 2, 2]
  """
  for k in range(len(items)-1, 0, -1):
    swapped = False
    for i in range(k, 0, -1):
      if items[i]<items[i-1]:
        items[i], items[i-1] = items[i-1], items[i]
        swapped = True
 
    for i in range(k):
      if items[i] > items[i+1]:
        items[i], items[i+1] = items[i+1], items[i]
        swapped = True
 
    if not swapped:
      return items
  return items

