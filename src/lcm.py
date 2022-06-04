def lcm(a, b):
    """
    Find the least common multiple of two numbers
    math.lcm() introduced with Python 3.9
    anaconda/2021b -> Python 3.8.11
    """
    i = 1
    if a > b:
        c = a
        d = b
    else:
        c = b
        d = a
    while True:
        if ((c * i) / d).is_integer():
            return int(c * i)
        i += 1;

