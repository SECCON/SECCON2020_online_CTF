def decrypt(c, d, n):
    size = n.bit_length() // 2

    c_high, c_low = c
    b = (c_low**2 - c_high**3) % n
    EC = EllipticCurve(Zmod(n), [0, b])
    m_high, m_low = (EC((c_high, c_low)) * d).xy()
    m_high, m_low = int(m_high), int(m_low)

    return (m_high << size) | m_low


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


def solve(n, e, plow):
    low_size = int(plow).bit_length()
    approx_size = (int(n).bit_length() // 2 - low_size) // 2 - 8
    print("known: {}, approx: {}".format(low_size, approx_size))
    for cov in covergents(e, n):
        x, y = cov

        if x == 0:
            continue

        if x * x > n:
            continue

        u = round(e*y / x - n - 1)
        v = round(sqrt(abs(u**2 - 4 * n)))

        if u < 0:
            continue

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

exec(open("output.txt").read())

# set_verbose(2)

for param in ciphertexts:
    n, e, c, hint = param["n"], param["e"], param["c"], param["hint"]
    p, q = solve(n, e, hint)
    d = inverse_mod(e, (p+1)*(q+1))
    masked_flag = masked_flag ^^ decrypt(c, d, int(n))

print(bytes.fromhex(hex(masked_flag)[2:]))
