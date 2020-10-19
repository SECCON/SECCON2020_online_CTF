from ptrlib import *

cipher = b'#\x12vF\xc5\xa5\xbeT\xf6\xe8"z\xc9\x93\xb4]^\x17]\x053\xcd/\x02\xe6k\xc4B\xe8\xa0\x10mx\xc2\xf4S*\xecyr9\xfb\x91T\x1fB\xacI7:\xabI\x12X\x85G\x05\xbb\x18W[\xfb@\x05'

key = 0x6d35bcd
def f(x):
    global key
    key = ((key * 0x77f - 0x32a) % 0x100000000) % 0x305eb3ea
    return 0xffffffff ^ key ^ x

def decrypt(s):
    output = b''
    for block in chunks(s, 8, b'\x00'):
        a, b = u32(block[0:4]), u32(block[4:8])
        for i in range(3):
            a, b = b, a ^ f(b)
        output += p32(a) + p32(b)
    return output

print(decrypt(cipher))

