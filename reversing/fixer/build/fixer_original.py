FIX = (lambda a: (lambda b: a(lambda c: b(b)(c)))(lambda b: a(lambda c: b(b)(c))))
MC = (lambda a: lambda b: b - 10 if b > 266 else a(a(b+11)))
FACT = (lambda a: lambda b: 1 if b == 0 else ((b+1) * a(b-1) + 7) & 0xff)
MAP = (lambda f: lambda b: lambda c: [] if len(c) == 0 else [b(ord(c[0])-0x41)] + (f(b)(c[1:])))
REDUCE = (lambda f: lambda b: lambda c: lambda d: d if len(c) == 0 else b(f(b)(c[1:])(d))(c[0]))
REDF = (lambda a: lambda b: a * FIX(MC)(b) + b)
EQ = (lambda a: lambda b: a == b)
f = lambda s: EQ(0x1f8dd85698fb84cc77d5d5046a176f6b51a9531952d4409d133ff48b68f)(FIX(REDUCE)(REDF)(FIX(MAP)(FIX(FACT))(s))(0))

g = FIX(MAP)(FIX(FACT))
# TODO: 消す
assert(len(set(g("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))) == 26)
for i in range(0x100):
    assert(FIX(MC)(i) == 0x101)
l = f("MYCJILJCZEKRDNNWZUGSEZQSKKPKZA")
print(l)
