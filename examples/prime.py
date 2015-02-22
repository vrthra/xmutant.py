def prime(input):
    for n in range(2, input):
        if input%n == 0:
            return False
    return True
