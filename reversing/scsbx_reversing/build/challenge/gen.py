from ptrlib import *
flag = b"SECCON{TfuRYYVaz8Us696t3JWNxZZPsXEmdL7cCmgzpgxXKarUOnIwhSj9tQ}\n"

key = 0x6d35bcd
def f(x):
    global key
    key = ((key * 0x77f - 0x32a) % 0x100000000) % 0x305eb3ea
    return 0xffffffff ^ key ^ x

def encrypt(s):
    output = b''
    for block in chunks(s, 8, b'\x00'):
        a, b = u32(block[0:4]), u32(block[4:8])
        for i in range(3):
            a, b = b, a ^ f(b)
        output += p32(a) + p32(b)
    return output

#for block in chunks(encrypt(flag), 4):
#    print(hex(u32(block)))
print(encrypt(flag))
