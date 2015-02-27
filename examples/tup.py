import typ
@typ.typ(a=(int,int))
def func2(a):
    """
    >>> func2((4,3))
    False
    >>> func2((8,2))
    True
    """
    if a[0] > 6:
        return True
    return False

