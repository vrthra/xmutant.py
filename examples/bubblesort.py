# source: http://danishmujeeb.com/blog/2014/01/basic-sorting-algorithms-implemented-in-python
import typ

@typ.typ(items=[int])
def bubble_sort(items):
    """
    >>> bubble_sort([])
    []
    >>> bubble_sort([1])
    [1]
    >>> bubble_sort([2,1])
    [1, 2]
    >>> bubble_sort([1,2])
    [1, 2]
    >>> bubble_sort([1,2,2])
    [1, 2, 2]
    """
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]     # Swap!
    return items

