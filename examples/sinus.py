from math import factorial

def my_sin(x):
    sign = -1
    p = d = 1
    i = sinx = 0

    while d > 0.00001: 
        d = (x**p)/float(factorial(p))
        sinx += ((sign**i)*d)
        i+=1
        p+=2

    return sinx
