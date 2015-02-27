import typ
@typ.typ(a={int})
def func2(a):
    """
    >>> func2({4,5})
    False
    >>> func2({8,9})
    True
    """
    if list(a)[0] > 6:
        return True
    return False

