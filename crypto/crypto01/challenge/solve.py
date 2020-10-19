from sage.all import *


def contfrac(x, y):
    """
    calculate continuated fraction of x/y
    """
    while y:
        a = x // y
        yield a
        x, y = y, x - a * y


def covergents(e, n):
    numerator, denominator = 1, 0
    numerator2, denominator2 = 0, 1
    for x in contfrac(e, n):
        numerator, numerator2 = x * numerator + numerator2, numerator
        denominator, denominator2 = x * denominator + denominator2, denominator

        yield numerator, denominator


def solve(n, e, plow, x, y, size, hint_size):
    approx_size = (size - hint_size) // 2 - 8
    low_size = int(plow).bit_length()
    y, x = x, y
    # print("known: {}, approx: {}, need: {}, guess: {}".format(hint_size, approx_size, size, size - approx_size - low_size))

    u = round(e*y / x - n - 1)
    v = round(sqrt(abs(u**2 - 4 * n)))

    p_ = Integer(u + v) // 2
    size = p_.nbits() - approx_size
    p_ = (p_ >> size) << size

    PR, x = PolynomialRing(Zmod(n), name="x").objgen()
    f = x*2**low_size + plow + p_
    f = f.monic()

    roots = f.small_roots(X=2**(size - low_size), beta=0.5, epsilon=0.05)
    for r in roots:
        p = int(p_ + plow + r * 2 ** low_size)
        if n % p == 0:
            return p, n // p
    return None, None
