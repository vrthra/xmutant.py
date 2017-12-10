import typ

@typ.typ(items=[int], left=int, mid=int, right=int)
def merge(items, left, mid, right):
  """
  Merge fuction
  """
  #Copy array
  copy_list = []
  i, j = left, mid + 1
  ind = left
  
  while ind < right+1:
    
    #if left array finish merging, copy from right side
    if i > mid:
      copy_list.append(items[j])
      j +=1
    #if right array finish merging, copy from left side
    elif j > right:
      copy_list.append(items[i])
      i +=1
    #Check if right array value is less than left one
    elif items[j] < items[i]:
      copy_list.append(items[j])
      j +=1
    else:
      copy_list.append(items[i])
      i +=1
    ind +=1
    
  ind=0
  for x in (range(left,right+1)):
    items[x] = copy_list[ind]
    ind += 1
  
@typ.typ(items=[int])
def merge_sort(items):
  """
  >>> merge_sort([])
  []
  >>> merge_sort([1])
  [1]
  >>> merge_sort([2,1])
  [1, 2]
  >>> merge_sort([1,2])
  [1, 2]
  >>> merge_sort([1,2,2])
  [1, 2, 2]
  """
  if len(items) == 0:
    return []
  left = 0
  right = len(items) - 1
  factor = 2
  temp_mid = 0
  #Main loop to iterate over the array by 2^n.
  while 1:
    index = 0
    left = 0
    right = len(items) - (len(items) % factor) - 1
    mid = (factor / 2) - 1
    
    #Auxiliary array to merge subdivisions
    while index < right:
      temp_left = index
      temp_right = temp_left + factor -1
      mid2 = (temp_right +temp_left) / 2
      merge(items, temp_left, mid2, temp_right)
      index = (index + factor)
    
    #Chek if there is something to merge from the remaining
    #Sub-array created by the factor
    if len(items) % factor and temp_mid !=0:
      #merge sub array to later be merged to the final array
      merge(items, right +1, temp_mid, len(items)-1)
      #Update the pivot
      mid = right
    #Increase the factor
    factor = factor * 2
    temp_mid = right
    
    #Final merge, merge subarrays created by the subdivision
    #of the factor to the main array.
    if factor > len(items) :
      mid = right
      right = len(items)-1
      merge(items, 0, mid, right)
      break
  return items

