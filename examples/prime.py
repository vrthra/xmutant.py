def prime(input):
    """
    >>> prime(3)
    True
    """
    for n in range(2, input):
        if input%n == 0:
            return False
    return True
