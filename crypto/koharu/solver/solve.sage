with open("output.txt") as f:
    line = f.readline()
    p = int(line.split("=")[1])

    PR.<x> = PolynomialRing(GF(p))
    PQ = sage_eval(f.readline().split("=")[1], locals={'x': x})
    f.readline() # pass R
    c = sage_eval(f.readline().split("=")[1], locals={'x': x})

pq = factor(PQ)
P = pq[0][0]
Q = pq[1][0]

print(P)
print(Q)

NP = p ** P.degree()
NQ = p ** Q.degree()
m = ""

from tqdm import tqdm

for f in tqdm(c):
    if power_mod(f, (NP-1)//2, P) == 1 and power_mod(f, (NQ-1)//2, Q) == 1:
        m += "1"
    else:
        m += "0"

m = int(m[::-1],2 )
print(bytes.fromhex(hex(m)[2:]))
