exec(open("output.txt").read())

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

PR.<x> = PolynomialRing(Zmod(n))

f1 = (3*x^2 + a)^2 - 2*x*4*(x^3 + a*x + b) - Q[0]*4*(x^3 + a*x + b)
f2 = (x + t)^65537 - c

r = gcd(f1, f2)
k = inverse_mod(Integer(r[1]), n)
m = -k * r[0]
print(bytes.fromhex(hex(m)[2:]))

