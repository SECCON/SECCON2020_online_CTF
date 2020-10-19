# Brief Documentation for SCSBX

## SCSBX
### What is SCSBX?
SCSBX is a virtual machine for SCArch-32, a virtual architecture
designed for SECCON Online CTF 2020.
SCArch-32 is a stack machine with 32-bit address space.

### Direct Memory Access
SCSBX allows the program to directly access to the host memory.
This may sound dangerous but the program can only use the 32-bit
address space. Since SCSBX runs on a 64-bit machine with PIE enabled,
there's no way the user can read/write the VM memory directly.

## Design
### Instruction
Every instruction except for `push` is 1-byte long.
`push` accepts a 4-byte value to push into the stack.
**SCSBX is proudly open-sourced!**
Check the source code for more details.

### Memory Layout
The user-land memory layout of SCSBX looks like the following.
```
0x00000000 +-------------------+
           |                   |
           |     Free Space    |
0x55540000 +-------------------+
           | Machine Code (R-) |
           +-------------------+
           |                   |
           |     Free Space    |
           |                   |
0xfffe0000 +-------------------+
           |     Stack (RW)    |
0xffff0000 +-------------------+  ^^^ user-space ^^^
           |  Guard Page (--)  |
0xffffffff +-------------------+  vvv  VM-space  vvv
           |    VM instance    |
           |        ...        |
```
The machine code and the stack are mapped to 0x55540000 and
0xfffe0000 respectively. The code region is only readable.
The stack region is both readable and writable. The user can
directly request memory resource of the host by `sys_map`
instruction. (Use `sys_unmap` to unmap the allocated region.)
The user needs to give `sys_map` the address to allocate.
Be noticed that the addresses between 0xffff0000 and 0xffffffff
can't be used as the region is reserved for Guard Page.
The Guard Page ensures that SCSBX throws an exception if the stack
is used up.
