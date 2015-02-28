import typ
@typ.typ(items=[int])
def tim_sort(items):
  """
  >>> tim_sort([])
  []
  >>> tim_sort([1])
  [1]
  >>> tim_sort([2,1])
  [1, 2]
  >>> tim_sort([1,2])
  [1, 2]
  >>> tim_sort([1,2,2])
  [1, 2, 2]
  """
  '''Sort function for timsort'''
  timsort_object = Timsort(items)
  timsort_object.sort(low = 0, high = len(items))
  return items
  
@typ.typ(list1=[int], base1=int, list2=[int], base2=int, length=int)
def array_copy(list1, base1, list2, base2, length):
  '''
  Copy from list1 to list2 at offsets base1 and base2, for length elements.
  Like Java's System.arraycopy.
  '''

  if id(list1) == id(list2):
    if base1 < base2:
      copy_forward = False
    else:
      copy_forward = True
  else:
    copy_forward = True

  if copy_forward:
    for offset in xrange(length):
      list2[base2 + offset] = list1[base1 + offset]
  else:
    for offset in xrange(length-1, -1, -1):
      list2[base2 + offset] = list1[base1 + offset]


@typ.typ(key=int, items=[int], base=int, length=int, hint=int)
def gallop_right(key, items, base, length, hint):
  '''
  Like gallop_left, except that if the range contains an element equal to
  key, gallop_right returns the index after the rightmost equal element.
  
  @param key the key whose insertion point to search for
  @param items the array in which to search
  @param base the index of the first element in the range
  @param length the length of the range; must be > 0
  @param hint the index at which to begin the search, 0 <= hint < number.
   The closer hint is to the result, the faster this method will run.
  @return the int k,  0 <= k <= number such that items[b + k - 1] <= key < items[b + k]
  '''
  assert length > 0 and hint >= 0 and hint < length

  offset = 1
  last_offset = 0
  if cmp(key, items[base + hint]) < 0:
    max_offset = hint + 1
    while offset < max_offset and cmp(key, items[base + hint - offset]) < 0:
      last_offset = offset
      offset = (offset << 1) + 1
      if offset <= 0:
        offset = max_offset
    if offset > max_offset:
      offset = max_offset

    tmp = last_offset
    last_offset = hint - offset
    offset = hint - tmp
  else:
    max_offset = length - hint
    while offset < max_offset and cmp(key, items[base + hint + offset]) >= 0:
      last_offset = offset
      offset = (offset << 1) + 1
      if offset <= 0:
        offset = max_offset
    if offset > max_offset:
      offset = max_offset

    last_offset += hint
    offset += hint
  assert -1 <= last_offset and last_offset < offset and offset <= length

  last_offset += 1
  while last_offset < offset:
    midpoint = last_offset + ((offset - last_offset) / 2)

    if cmp(key, items[base + midpoint]) < 0:
      offset = midpoint
    else:
      last_offset = midpoint + 1
  assert last_offset == offset
  return offset

@typ.typ(key=int, items=[int], base=int, length=int, hint=int)
def gallop_left(key, items,  base, length, hint):
  '''
  Locates the position at which to insert the specified key into the
  specified sorted range; if the range contains an element equal to key,
  returns the index of the leftmost equal element.
  
  @param key the key whose insertion point to search for
  @param items the array in which to search
  @param base the index of the first element in the range
  @param length the length of the range; must be > 0
  @param hint the index at which to begin the search, 0 <= hint < number.
   The closer hint is to the result, the faster this method will run.
  @param c the comparator used to order the range, and to search
  @return the int k,  0 <= k <= number such that items[b + k - 1] < key <= items[b + k],
  pretending that items[b - 1] is minus infinity and items[b + number] is infinity.
  In other words, key belongs at index b + k; or in other words,
  the first k elements of items should precede key, and the last number - k
  should follow it.
  '''
  assert length > 0 and hint >= 0 and hint < length
  last_offset = 0
  offset = 1
  if cmp(key, items[base + hint]) > 0:
    max_offset = length - hint
    while offset < max_offset and cmp(key, items[base + hint + offset]) > 0:
      last_offset = offset
      offset = (offset << 1) + 1
      if offset <= 0:
        offset = max_offset
    if offset > max_offset:
      offset = max_offset

    last_offset += hint
    offset += hint
  else:
    max_offset = hint + 1
    while offset < max_offset and cmp(key, items[base + hint - offset]) <= 0:
      last_offset = offset
      offset = (offset << 1) + 1
      if offset <= 0:
        offset = max_offset
    if offset > max_offset:
      offset = max_offset

    tmp = last_offset
    last_offset = hint - offset
    offset = hint - tmp
  assert -1 <= last_offset and last_offset < offset and offset <= length

  last_offset += 1
  while last_offset < offset:
    midpoint = last_offset + ((offset - last_offset) / 2)

    if cmp(key, items[base + midpoint]) > 0:
      last_offset = midpoint + 1
    else:
      offset = midpoint
  assert last_offset == offset
  return offset

@typ.typ(items=[int], low=int, high=int, start=int)
def binary_sort(items,  low,  high,  start):
  '''
  Sorts the specified portion of the specified array using a binary
  insertion sort.  This is the best method for sorting small numbers
  of elements.  It requires O(n log n) compares, but O(n^2) data
  movement (worst case).
  
  If the initial part of the specified range is already sorted,
  this method can take advantage of it: the method assumes that the
  elements from index {@code low}, inclusive, to {@code start},
  exclusive are already sorted.
  
  @param items the array in which a range is to be sorted
  @param low the index of the first element in the range to be sorted
  @param high the index after the last element in the range to be sorted
  @param start the index of the first element in the range that is
    not already known to be sorted (@code low <= start <= high}
  '''
  assert low <= start and start <= high
  if start == low:
    start += 1
  for start in xrange(start, high):
    pivot = items[start]

    left = low
    right = start
    assert left <= right
    while left < right:
      mid = (left + right) / 2
      if cmp(pivot, items[mid]) < 0:
        right = mid
      else:
        left = mid + 1
    assert left == right

    number = start - left
    array_copy(items, left, items, left + 1, number)
    items[left] = pivot

@typ.typ(items=[int], low=int, high=int)
def reverse_range(items, low, high):
  '''
  Reverse the specified range of the specified array.
  
  @param items the array in which a range is to be reversed
  @param low the index of the first element in the range to be reversed
  @param high the index after the last element in the range to be reversed
  '''
  high -= 1
  while low < high:
    items[low], items[high] = items[high], items[low]
    low += 1
    high -= 1

@typ.typ(items=[int], low=int, high=int)
def count_run_and_make_ascending(items, low, high):
  '''
  Returns the length of the run beginning at the specified position in
  the specified array and reverses the run if it is descending (ensuring
  that the run will always be ascending when the method returns).
  
  A run is the longest ascending sequence with:
  
    items[low] <= items[low + 1] <= items[low + 2] <= ...
  
  or the longest descending sequence with:
  
    items[low] >  items[low + 1] >  items[low + 2] >  ...
  
  For its intended use in a stable mergesort, the strictness of the
  definition of "descending" is needed so that the call can safely
  reverse a descending sequence without violating stability.
  
  @param items the array in which a run is to be counted and possibly reversed
  @param low index of the first element in the run
  @param high index after the last element that may be contained in the run.
   It is required that @code{low < high}.
  @return  the length of the run beginning at the specified position in
        the specified array
  '''
  assert low < high
  run_high = low + 1
  if run_high == high:
    return 1

  if cmp(items[run_high], items[low]) < 0:
    run_high += 1
    while run_high < high and cmp(items[run_high], items[run_high - 1]) < 0:
      run_high += 1
    reverse_range(items, low, run_high)
  else:
    run_high += 1
    while run_high < high and cmp(items[run_high], items[run_high - 1]) >= 0:
      run_high += 1

  return run_high - low

class Timsort:
  '''Class for timsort'ing'''

  
  def __init__(self, items):
    self.min_merge = 32
    self.initial_min_gallop = 7
    self.stack_size = 0

    self.initial_tmp_storage_length = 256

    self.run_base = []
    self.run_len = []

    self.min_gallop = self.initial_min_gallop

    self.items = items

    length = len(items)
    if length < self.initial_tmp_storage_length * 2:
      ternary = length / 2
    else:
      ternary = self.initial_tmp_storage_length
    self.tmp = range(ternary)

    if length < 120:
      self.stack_len = 5
    elif length < 1542:
      self.stack_len = 10
    elif length < 119151:
      self.stack_len = 19
    else:
      self.stack_len = 40
    self.run_base = range(self.stack_len)
    self.run_len = range(self.stack_len)

  def sort(self, low, high):
    '''sort method - perform a sort :)'''
    items = self.items
    range_check(len(items), low, high)
    num_remaining = high - low
    if num_remaining < 2:
      return

    if num_remaining < self.min_merge:
      initial_run_len = count_run_and_make_ascending(items, low, high)
      binary_sort(self.items, low, high, low + initial_run_len)
      return

    min_run = self.min_run_length(num_remaining)
    while True:
      run_len = count_run_and_make_ascending(items, low, high)

      if run_len < min_run:
        if num_remaining <= min_run:
          ternary = num_remaining
        else:
          ternary = min_run
        force = ternary
        binary_sort(self.items, low, low + force, low + run_len)
        run_len = force

      self.push_run(low, run_len)
      self.merge_collapse()

      low += run_len
      num_remaining -= run_len
      if num_remaining == 0:
        break

    assert low == high
    self.merge_force_collapse()
    assert self.stack_size == 1

  def min_run_length(self, number):
    '''
    Returns the minimum acceptable run length for an array of the specified
    length. Natural runs shorter than this will be extended with
    {@link #binary_sort}.
    
    Roughly speaking, the computation is:
    
     If number < self.min_merge, return number (it's too small to bother with fancy stuff).
     Else if number is an exact power of 2, return self.min_merge/2.
     Else return an int k, self.min_merge/2 <= k <= self.min_merge, such that number/k
      is close to, but strictly less than, an exact power of 2.
    
    For the rationale, see listsort.txt.
    
    @param number the length of the array to be sorted
    @return the length of the minimum run to be merged
    '''

    assert number >= 0
    low_bit = 0
    while number >= self.min_merge:
      low_bit |= (number & 1)
      number >>= 1
    return number + low_bit

  def push_run(self, run_base, run_len):
    '''
    Pushes the specified run onto the pending-run stack.
    
    @param self.run_base index of the first element in the run
    @param self.run_len  the number of elements in the run
    '''
    self.run_base[self.stack_size] = run_base
    self.run_len[self.stack_size] = run_len
    self.stack_size += 1

  def merge_collapse(self):
    '''
    Examines the stack of runs waiting to be merged and merges adjacent runs
    until the stack invariants are reestablished:
    
     1. self.run_len[i - 3] > self.run_len[i - 2] + self.run_len[i - 1]
     2. self.run_len[i - 2] > self.run_len[i - 1]
    
    This method is called each time a new run is pushed onto the stack,
    so the invariants are guaranteed to hold for i < self.stack_size upon
    entry to the method.
    '''
    while self.stack_size > 1:
      number = self.stack_size - 2
      if number > 0 and self.run_len[number-1] <= self.run_len[number] + self.run_len[number+1]:
        if self.run_len[number - 1] < self.run_len[number + 1]:
          number -= 1
        self.merge_at(number)
      elif self.run_len[number] <= self.run_len[number + 1]:
        self.merge_at(number)
      else:
        break

  def merge_force_collapse(self):
    '''
    Merges all runs on the stack until only one remains.  This method is
    called once, to complete the sort.
    '''
    while self.stack_size > 1:
      number = self.stack_size - 2
      if number > 0 and self.run_len[number - 1] < self.run_len[number + 1]:
        number -= 1
      self.merge_at(number)

  def merge_at(self,  i):
    '''
    Merges the two runs at stack indices i and i+1.  Run i must be
    the penultimate or antepenultimate run on the stack.  In other words,
    i must be equal to self.stack_size-2 or self.stack_size-3.
    
    @param i stack index of the first of the two runs to merge
    '''
    assert self.stack_size >= 2
    assert i >= 0
    assert i == self.stack_size - 2 or i == self.stack_size - 3

    base1 = self.run_base[i]
    len1 = self.run_len[i]
    base2 = self.run_base[i + 1]
    len2 = self.run_len[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2

    self.run_len[i] = len1 + len2
    if i == self.stack_size - 3:
      self.run_base[i + 1] = self.run_base[i + 2]
      self.run_len[i + 1] = self.run_len[i + 2]
    self.stack_size -= 1

    k = gallop_right(self.items[base2], self.items, base1, len1, 0)
    assert k >= 0
    base1 += k
    len1 -= k
    if len1 == 0:
      return

    len2 = gallop_left(self.items[base1 + len1 - 1], self.items, base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
      return

    if len1 <= len2:
      self.merge_low(base1, len1, base2, len2)
    else:
      self.merge_high(base1, len1, base2, len2)

  def merge_low(self, base1, len1, base2, len2):
    '''
    Merges two adjacent runs in place, in a stable fashion.  The first
    element of the first run must be greater than the first element of the
    second run (items[base1] > items[base2]), and the last element of the first run
    (items[base1 + len1-1]) must be greater than all elements of the second run.
    
    For performance, this method should be called only when len1 <= len2
    its twin, merge_high should be called if len1 >= len2.  (Either method
    may be called if len1 == len2.)
    
    @param base1 index of first element in first run to be merged
    @param len1  length of first run to be merged (must be > 0)
    @param base2 index of first element in second run to be merged
      (must be aBase + aLen)
    @param len2  length of second run to be merged (must be > 0)
    '''
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2

    items = self.items
    tmp = self.ensure_capacity(len1)
    array_copy(items, base1, tmp, 0, len1)

    cursor1 = 0
    cursor2 = base2
    dest = base1

    items[dest] = items[cursor2]
    dest += 1
    cursor2 += 1
    len2 -= 1
    if len2 == 0:
      array_copy(tmp, cursor1, items, dest, len1)
      return
    if len1 == 1:
      array_copy(items, cursor2, items, dest, len2)
      items[dest + len2] = tmp[cursor1]
      return

    min_gallop = self.min_gallop

    loops_done = False
    while True:
      count1 = 0
      count2 = 0

      while True:
        assert len1 > 1 and len2 > 0
        if cmp(items[cursor2], tmp[cursor1]) < 0:
          items[dest] = items[cursor2]
          dest += 1
          cursor2 += 1
          count2 += 1
          count1 = 0
          len2 -= 1
          if len2 == 0:
            loops_done = True
            break
        else:
          items[dest] = tmp[cursor1]
          dest += 1
          cursor1 += 1
          count1 += 1
          count2 = 0
          len1 -= 1
          if len1 == 1:
            loops_done = True
            break
        if (count1 | count2) >= min_gallop:
          break
      if loops_done:
        break

      while True:
        assert len1 > 1 and len2 > 0
        count1 = gallop_right(items[cursor2], tmp, cursor1, len1, 0)
        if count1 != 0:
          array_copy(tmp, cursor1, items, dest, count1)
          dest += count1
          cursor1 += count1
          len1 -= count1
          if len1 <= 1:
            loops_done = True
            break
        items[dest] = items[cursor2]
        dest += 1
        cursor2 += 1
        len2 -= 1
        if len2 == 0:
          loops_done = True
          break

        count2 = gallop_left(tmp[cursor1], items, cursor2, len2, 0)
        if count2 != 0:
          array_copy(items, cursor2, items, dest, count2)
          dest += count2
          cursor2 += count2
          len2 -= count2
          if len2 == 0:
            loops_done = True
            break
        items[dest] = tmp[cursor1]
        dest += 1
        cursor1 += 1
        len1 -= 1
        if len1 == 1:
          loops_done = True
          break
        min_gallop -= 1

        if not (count1 >= self.initial_min_gallop | count2 >= self.initial_min_gallop):
          break

      if loops_done:
        break

      if min_gallop < 0:
        min_gallop = 0
      min_gallop += 2

    if min_gallop < 1:
      ternary = 1
    else:
      ternary = min_gallop
    self.min_gallop = ternary

    if len1 == 1:
      assert len2 > 0
      array_copy(items, cursor2, items, dest, len2)
      items[dest + len2] = tmp[cursor1]
    elif len1 == 0:
      raise exceptions.ValueError, "Comparison function violates its general contract!"
    else:
      assert len2 == 0
      assert len1 > 1
      array_copy(tmp, cursor1, items, dest, len1)

  def merge_high(self, base1, len1, base2, len2):
    '''
    Like merge_low, except that this method should be called only if
    len1 >= len2; merge_low should be called if len1 <= len2.  (Either method
    may be called if len1 == len2.)
    
    @param base1 index of first element in first run to be merged
    @param len1  length of first run to be merged (must be > 0)
    @param base2 index of first element in second run to be merged
      (must be aBase + aLen)
    @param len2  length of second run to be merged (must be > 0)
    '''

    assert len1 > 0 and len2 > 0 and base1 + len1 == base2

    items = self.items
    tmp = self.ensure_capacity(len2)
    array_copy(items, base2, tmp, 0, len2)

    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1

    items[dest] = items[cursor1]
    dest -= 1
    cursor1 -= 1
    len1 -= 1
    if len1 == 0:
      array_copy(tmp, 0, items, dest - (len2 - 1), len2)
      return
    if len2 == 1:
      dest -= len1
      cursor1 -= len1
      array_copy(items, cursor1 + 1, items, dest + 1, len1)
      items[dest] = tmp[cursor2]
      return

    min_gallop = self.min_gallop

    loops_done = False
    while True:
      count1 = 0
      count2 = 0

      while True:
        assert len1 > 0 and len2 > 1
        if cmp(tmp[cursor2], items[cursor1]) < 0:
          items[dest] = items[cursor1]
          dest -= 1
          cursor1 -= 1
          count1 += 1
          count2 = 0
          len1 -= 1
          if len1 == 0:
            loops_done = True
            break
        else:
          items[dest] = tmp[cursor2]
          dest -= 1
          cursor2 -= 1
          count2 += 1
          count1 = 0
          len2 -= 1
          if len2 == 1:
            loops_done = True
            break
        if not ((count1 | count2) < min_gallop):
          break

      if loops_done:
        break

      while True:
        assert len1 > 0 and len2 > 1
        count1 = len1 - gallop_right(tmp[cursor2], items, base1, len1, len1 - 1)
        if count1 != 0:
          dest -= count1
          cursor1 -= count1
          len1 -= count1
          array_copy(items, cursor1 + 1, items, dest + 1, count1)
          if len1 == 0:
            loops_done = True
            break
        items[dest] = tmp[cursor2]
        dest -= 1
        cursor2 -= 1
        len2 -= 1
        if len2 == 1:
          loops_done = True
          break

        count2 = len2 - gallop_left(items[cursor1], tmp, 0, len2, len2 - 1)
        if count2 != 0:
          dest -= count2
          cursor2 -= count2
          len2 -= count2
          array_copy(tmp, cursor2 + 1, items, dest + 1, count2)
          if len2 <= 1:
            loops_done = True
            break
        items[dest] = items[cursor1]
        dest -= 1
        cursor1 -= 1
        len1 -= 1
        if len1 == 0:
          loops_done = True
          break
        min_gallop -= 1
        if not (count1 >= self.initial_min_gallop | count2 >= self.initial_min_gallop):
          break

      if loops_done:
        break

      if min_gallop < 0:
        min_gallop = 0
      min_gallop += 2

    if min_gallop < 1:
      ternary = 1
    else:
      ternary = min_gallop
    self.min_gallop = ternary

    if len2 == 1:
      assert len1 > 0
      dest -= len1
      cursor1 -= len1
      array_copy(items, cursor1 + 1, items, dest + 1, len1)
      items[dest] = tmp[cursor2]
    elif len2 == 0:
      raise exceptions.ValueError, "Comparison function violates its general contract!"
    else:
      assert len1 == 0
      assert len2 > 0
      array_copy(tmp, 0, items, dest - (len2 - 1), len2)

  def ensure_capacity(self, min_capacity):
    '''
    Ensures that the external array tmp has at least the specified
    number of elements, increasing its size if necessary.  The size
    increases exponentially to ensure amortized linear time complexity.
    
    @param min_capacity the minimum required capacity of the tmp array
    @return tmp, whether or not it grew
    '''
    if len(self.tmp) < min_capacity:
      new_size = min_capacity
      new_size |= new_size >> 1
      new_size |= new_size >> 2
      new_size |= new_size >> 4
      new_size |= new_size >> 8
      new_size |= new_size >> 16
      new_size += 1

      if new_size < 0:
        new_size = min_capacity
      else:
        new_size = min(new_size, len(self.items) / 2)

      self.tmp = range(new_size)
    return self.tmp

@typ.typ(array_len=int, from_index=int, to_index=int)
def range_check(array_len, from_index, to_index):
  '''
  Checks that from_index and to_index are in range, and throws an
  appropriate exception if they aren't.
  
  @param array_len the length of the array
  @param from_index the index of the first element of the range
  @param to_index the index after the last element of the range
  @throws IllegalArgumentException if from_index > to_index
  @throws ArrayIndexOutOfBoundsException if from_index < 0
     or to_index > array_len
  '''
  if from_index > to_index:
    raise exceptions.ValueError, "from_index(" + from_index + ") > to_index(" + to_index+")"
  if from_index < 0:
    raise exceptions.IndexError, str(from_index)
  if to_index > array_len:
    raise exceptions.IndexError, str(to_index)

