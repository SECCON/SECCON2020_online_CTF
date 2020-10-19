while True:
    p = random_prime(1<<64)
    if is_prime((p+1) // 2):
        break

with open("flag.txt", "rb") as f:
    flag = f.read()
flag = int.from_bytes(flag, "big")


PR.<x> = PolynomialRing(GF(p))
while True:
    P = PR.random_element(degree=64)
    if P.is_irreducible():
        break

while True:
    Q = PR.random_element(degree=64)
    if Q.is_irreducible():
        break

NP = p**P.degree()
NQ = p**Q.degree()

while True:
    R = PR.random_element(degree=64)
    if power_mod(R, (NP-1)//2, P) != 1 and power_mod(R, (NQ-1)//2, Q) != 1:
        break

PQ = P*Q
c = []
while flag:
    S = PR.random_element(degree=64)
    if flag & 1:
        c.append((S * S) % PQ)
    else:
        c.append((S * S * R) % PQ)
    flag = flag >> 1

print("p =", p)
print("PQ =", PQ)
print("R =", R)
print("c =", c)


