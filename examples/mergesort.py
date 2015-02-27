# source: http://danishmujeeb.com/blog/2014/01/basic-sorting-algorithms-implemented-in-python
import typ

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
    if len(items) > 1:

        mid = len(items) / 2        # Determine the midpoint and split
        left = items[0:mid]
        right = items[mid:]

        merge_sort(left)            # Sort left list in-place
        merge_sort(right)           # Sort right list in-place

        l, r = 0, 0
        for i in range(len(items)):     # Merging the left and right list

            lval = left[l] if l < len(left) else None
            rval = right[r] if r < len(right) else None

            if (lval and rval and lval < rval) or rval is None:
                items[i] = lval
                l += 1
            elif (lval and rval and lval >= rval) or lval is None:
                items[i] = rval
                r += 1
            else:
                raise Exception('Could not merge, sub arrays sizes do not match the main array')
    return items
