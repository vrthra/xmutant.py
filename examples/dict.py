import typ
@typ.typ(a={int:int})
def func2(a):
    """
    >>> func2({4:3})
    False
    >>> func2({8:8})
    True
    """
    if a[sorted(a.keys())[0]] > 6:
        return True
    return False

