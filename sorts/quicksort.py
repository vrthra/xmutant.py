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
  if len(items) == 0:
    return []
  left = 0
  right = len(items) -1
  temp_stack = []
  temp_stack.append((left,right))
  
  #Main loop to pop and push items until stack is empty
  while temp_stack:    
    pos = temp_stack.pop()
    right, left = pos[1], pos[0]
#--------------------------
    #Pivot first element in the array
    p = items[left]
    i = left + 1
    j = right
   
    while 1:
      while i <= j  and items[i] <= p:
        i +=1
      while j >= i and items[j] >= p:
        j -=1
      if j <= i:
        break
      #Exchange items
      items[i], items[j] = items[j], items[i]
    #Exchange pivot to the right position
    items[left], items[j] = items[j], items[left]
    piv = j
#--------------------------
    #If items in the left of the pivot push them to the stack
    if piv-1 > left:
      temp_stack.append((left,piv-1))
    #If items in the right of the pivot push them to the stack
    if piv+1 < right:
      temp_stack.append((piv+1,right))
  return items
 
