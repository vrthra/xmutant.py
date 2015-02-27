import typ
@typ.typ(a={int:int})
def func2(a):
    """
    >>> func2({4:5})
    False
    >>> func2({8:9})
    True
    """
    if a.keys()[0] > 6:
        return True
    return False

