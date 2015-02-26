import typ
@typ.typ(a=[int])
def func2(a):
    """
    >>> func2([4])
    False
    >>> func2([8])
    True
    """
    if a[0] > 6:
        return True
    return False

