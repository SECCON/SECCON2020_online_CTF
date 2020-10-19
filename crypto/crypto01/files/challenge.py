from sage.all import *
from flag import flag
from functools import reduce

def encrypt(m, e, n):
    n = int(n)
    size = n.bit_length() // 2
    m_low = m & ((1 << size) - 1)
    m_high = (m >> size)

    b = (m_low**2 - m_high**3) % n
    EC = EllipticCurve(Zmod(n), [0, b])

    return (EC((m_high, m_low)) * e).xy()

def decrypt(c, d, n):
    n = int(n)
    size = n.bit_length() // 2

    c_high, c_low = c
    b = (c_low**2 - c_high**3) % n
    EC = EllipticCurve(Zmod(n), [0, b])
    m_high, m_low = (EC((c_high, c_low)) * d).xy()
    m_high, m_low = int(m_high), int(m_low)

    return (m_high << size) | m_low

def gen_prime(size):
    p = random_prime(1 << size)
    while p % 3 != 2:
        p = random_prime(1 << size)

    q = random_prime(1 << size)
    while q % 3 != 2:
        q = random_prime(1 << size)

    if q > p:
        p, q = q, p

    return int(p), int(q)



SIZE = 512
HINTSIZE = 96
N = 3

flag = int.from_bytes(flag, "big")
assert flag < (1 << SIZE)

masks = [randint(1 << (SIZE-1), 1 << SIZE) for _ in range(N)]
masked_flag = reduce(lambda a, b: a ^ b, masks, flag)


count = 0
ciphertexts = []
while count < N:
    try:
        p, q = gen_prime(SIZE)
        n = p * q

        x = random_prime(int(n ** 0.40))
        y = random_prime(int(sqrt(2 * n // (144 * x*x))))
        zbound = -1 * int(round(((p-q) * (n ** 0.25) * y) / (3 * (p + q))))

        z_ = zbound + ((p + 1)*(q + 1)*y - zbound) % x
        e = ((p + 1) * (q + 1) * y - z_) // x
        d = inverse_mod(e, (p + 1)*(q + 1))

        assert (x*y*x*y < (2 * n // 144))
        assert (gcd(x, y) == 1)

        d = inverse_mod(e, (p+1)*(q+1))
        c = encrypt(masks[count], e, n)
        assert decrypt(c, d, n) == masks[count]

        ciphertexts.append({
            "n": n,
            "e": e,
            "c": c,
            "hint": p & ((1<<HINTSIZE)-1)
        })
        count += 1
    except KeyboardInterrupt:
        break
    except (ZeroDivisionError, OverflowError):
        pass


print("masked_flag = " ,masked_flag)
print("ciphertexts = ", ciphertexts)
