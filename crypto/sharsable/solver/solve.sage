# Overview
# This challenge is based on May's version of Wiener's Attack
# (https://www.math.uni-frankfurt.de/~dmst/teaching/WS2015/Vorlesung/Alex.May.pdf)
# But the attack can't be apply to the challenge because it has 2 exponents,
# so you have to extend the method of May.
# After LLL, choose 2 shortest vectors and reconstruct polynomial.
# then pick coefficients and decrypt ciphertext

import json
from binascii import unhexlify

problem = json.load(open('output'))

n = problem['n']
eA, cA = problem['A']
eB, cB = problem['B']

X = int(n^(0.16))
Y = X
Z = int(3 / sqrt(2) * sqrt(n) * X)

B = Matrix(ZZ, [[n*X, 0, 0], [0, n*Y, 0], [eA*X, eB*Y, Z]])
L = B.LLL()

c1 = B.solve_left(L[0])
c2 = B.solve_left(L[1])

PR.<x, y, z> = PolynomialRing(ZZ)

f = (c1[0]*n + c1[2]*eA)*x + (c1[1]*n + c1[2]*eB)*y + c1[2]*z
g = (c2[0]*n + c2[2]*eA)*x + (c2[1]*n + c2[2]*eB)*y + c2[2]*z

h = c2[2] * f - c1[2] * g
y0 = abs(h.coefficients()[0])
x0 = abs(h.coefficients()[1])
g = gcd(int(x0), int(y0))
x0 = x0 / g
y0 = y0 / g
print('x:', x0)
print('y:', y0)
print(unhexlify(hex(pow(cA, int(x0), n) * pow(cB, int(y0), n) % n)[2:]))
