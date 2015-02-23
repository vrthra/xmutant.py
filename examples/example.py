"""
Example Programs
"""
def func1(a):
    """
    This should fail mutation testing (we don't test edge cases of a=5, a=6)
    >>> args = [dict(min=0, max=100)]
    >>> func1(4)
    False
    >>> func1(8)
    True
    """
    if a > 6:
        return True
    return False
    
def func2(a):
    """
    This should fail mutation testing.
    
    >>> func2(4)
    False
    >>> func2(5)
    False
    """
    if a > 5:
        return True
    return False
 
def func3(a):
    """
    This should pass mutation testing.
    
    >>> func3(4)
    False
    >>> func3(5)
    False
    >>> func3(6)
    True
    """
    if a > 5:
        return True
    return False
 
def func4(a):
    """
    >>> skips = ['5 : swap 0']
    """
    if a > 5:
        return True
    return False

