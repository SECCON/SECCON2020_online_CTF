import re

s = input()
m = re.match(r'^SECCON{([A-Z]+)}$', s)
if not m:
    print('invalid flag')
else:
    s = m.group(1)
    f = lambda s: (lambda a: lambda b: a == b)(0x1f8dd85698fb84cc77d5d5046a176f6b51a9531952d4409d133ff48b68f)((lambda a: (lambda b: a(lambda c: b(b)(c)))(lambda b: a(lambda c: b(b)(c))))((lambda f: lambda b: lambda c: lambda d: d if len(c) == 0 else b(f(b)(c[1:])(d))(c[0])))((lambda a: lambda b: a * (lambda a: (lambda b: a(lambda c: b(b)(c)))(lambda b: a(lambda c: b(b)(c))))((lambda a: lambda b: b - 10 if b > 266 else a(a(b+11))))(b) + b))((lambda a: (lambda b: a(lambda c: b(b)(c)))(lambda b: a(lambda c: b(b)(c))))((lambda f: lambda b: lambda c: [] if len(c) == 0 else [b(ord(c[0])-0x41)] + (f(b)(c[1:]))))((lambda a: (lambda b: a(lambda c: b(b)(c)))(lambda b: a(lambda c: b(b)(c))))((lambda a: lambda b: 1 if b == 0 else ((b+1) * a(b-1) + 7) & 0xff)))(s))(0))
    if f(s):
        print('correct')
    else:
        print('wrong')
