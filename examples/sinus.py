from math import factorial

# hangs on mutant
def my_sin(x):
    """
    >>> my_sin(1)
    0.8416666666666667
    """
    sign = -1
    p = d = 1
    i = sinx = 0

    while d > 0.01:
        d = (x**p)/float(factorial(p))
        sinx += ((sign**i)*d)
        i+=1
        p+=2

    return sinx
