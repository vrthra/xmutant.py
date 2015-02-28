import typ

@typ.typ(items=[int])
def strand_sort(items):
  """
  >>> strand_sort([])
  []
  >>> strand_sort([1])
  [1]
  >>> strand_sort([2,1])
  [1, 2]
  >>> strand_sort([1,2])
  [1, 2]
  >>> strand_sort([1,2,2])
  [1, 2, 2]
  """
  nitems = len(items)
  sortedBins = []
  while( len(items) > 0 ):
      highest = float("-inf")
      newBin = []
      i = 0
      while( i < len(items) ):
          if( items[i] >= highest ):
              highest = items.pop(i)
              newBin.append( highest )
          else:
              i=i+1
      sortedBins.append(newBin)
   
  sorted = []
  while( len(sorted) < nitems ):
      lowBin = 0
      for j in range( 0, len(sortedBins) ):
          if( sortedBins[j][0] < sortedBins[lowBin][0] ):
              lowBin = j
      sorted.append( sortedBins[lowBin].pop(0) )
      if( len(sortedBins[lowBin]) == 0 ):
          del sortedBins[lowBin]
  return sorted
   
