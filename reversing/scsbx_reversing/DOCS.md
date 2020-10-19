# Documentation of SCSBX

## Design
### Basics
SCSBX is a Virtual Machine written for SECCON Online 2020.
The architecture is based on a stack machine.
Every instruction is 1-byte except for PUSH.

### Stack Region
The stack bottom locates at **0xfffe0000**.
The initial size of the stack is 0x10000.

### Code Region
The machine code is allocated at **0x55540000**.
This region is read-only.

## Instructions
### Stack Operation
#### PUSH
Machine Code:
```
20 XX XX XX XX
```
Instruction:
```c
stack[++TOP] = 0xXXXXXXXX;
```

#### POP
Machine Code:
```
21
```
Instruction:
```c
TOP--;
```

#### DUP
Machine Code:
```
22
```
Instruction:
```c
a = stack[TOP--];
stack[++TOP] = stack[TOP - a];
```

#### XCHG
Machine Code:
```
23
```
Instruction:
```c
a = stack[TOP--];
tmp = stack[TOP];
stack[TOP] = stack[TOP - a];
stack[TOP - a] = tmp;
```

#### LOAD
Machine Code:
```
24
```
Instruction:
```c
address = stack[TOP];
stack[TOP] = *(long*)address;
```

#### STORE8
Machine Code:
```
25
```
Instruction:
```c
address = stack[TOP--];
*(char*)address = (char)stack[TOP--];
```

#### STORE16
Machine Code:
```
26
```
Instruction:
```c
address = stack[TOP--];
*(short*)address = (short)stack[TOP--];
```

#### STORE32
Machine Code:
```
27
```
Instruction:
```c
address = stack[TOP--];
*(int*)address = (int)stack[TOP--];
```

### Branch Operation
#### JMP / RET
Machine Code:
```
30
```
Instruction:
```c
t = stack[TOP--];
PC = t;
```

#### JEQ
Machine Code:
```
31
```
Instruction:
```c
t = stack[TOP--];
f = stack[TOP--];
a = stack[TOP--];
b = stack[TOP--];
if (a == b) {
  PC = t;
} else {
  PC = f;
}
```

#### JGT
Machine Code:
```
32
```
Instruction:
```c
t = stack[TOP--];
f = stack[TOP--];
a = stack[TOP--];
b = stack[TOP--];
if (a > b) {
  PC = t;
} else {
  PC = f;
}
```

#### JGE
Machine Code:
```
33
```
Instruction:
```c
t = stack[TOP--];
f = stack[TOP--];
a = stack[TOP--];
b = stack[TOP--];
if (a > b) {
  PC = t;
} else {
  PC = f;
}
```

#### CALL
Machine Code:
```
34
```
Instruction:
```c
t = stack[TOP--];
stack[++TOP] = PC;
PC = t;
```

### Arithmetic Operation
You can use arithmetic operation over integers by changing 4X to 5X.

#### ADD
Machine Code:
```
40
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] += a;
```

#### SUB
Machine Code:
```
41
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] -= a;
```

#### MUL
Machine Code
```
42
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] *= a;
```

#### DIV
Machine Code
```
43
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] /= a;
```

#### MOD
Machine Code
```
44
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] %= a;
```

#### ABS
Machine Code
```
45
```
Instruction:
```c
stack[TOP] = stack[TOP] < 0 ? -stack[TOP] : stack[TOP];
```

#### NEG
Machine Code
```
46
```
Instruction:
```c
stack[TOP] = -stack[TOP];
```

#### ROUND
Machine Code
```
47
```
Instruction:
```c
stack[TOP] = (float)((int)stack[TOP]);
```

#### CEIL
Machine Code
```
48
```
Instruction:
```c
stack[TOP] = ceil((float)stack[TOP]);
```

#### FLOOR
Machine Code
```
49
```
Instruction:
```c
stack[TOP] = floor((float)stack[TOP]);
```

#### SQRT
Machine Code
```
4a
```
Instruction:
```c
stack[TOP] = sqrt((float)stack[TOP]);
```

#### SIN
Machine Code
```
4b
```
Instruction:
```c
stack[TOP] = sin((float)stack[TOP]);
```

#### COS
Machine Code
```
4c
```
Instruction:
```c
stack[TOP] = cos((float)stack[TOP]);
```

#### ATAN
Machine Code
```
4d
```
Instruction:
```c
stack[TOP] = atan((float)stack[TOP]);
```

#### POW
Machine Code
```
4e
```
Instruction:
```c
a = (float)stack[TOP--];
stack[TOP] = pow(a, (float)stack[TOP]);
```

#### LOG
Machine Code
```
4f
```
Instruction:
```c
stack[TOP] = ln(stack[TOP]);
```

### Logical Operation
#### NOT
Machine Code
```
50
```
Instruction:
```c
stack[TOP] ^= 0xffffffff;
```

#### AND
Machine Code
```
51
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] &= a;
```

#### OR
Machine Code
```
52
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] |= a;
```

#### XOR
Machine Code
```
53
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] ^= a;
```

#### SHL
Machine Code
```
54
```
Instruction:
```c
c = stack[TOP--];
stack[TOP] <<= c;
```

#### SHR
Machine Code
```
55
```
Instruction:
```c
c = stack[TOP--];
stack[TOP] >>= c;
```

### System Operation
#### read
Machine Code
```
60
```
Instruction:
```c
memmap_id = stack[TOP--];
addr = stack[TOP--];
size = stack[TOP--];
stack[++TOP] = __mem_read(memmap_id, addr, size);
```

#### write
Machine Code
```
61
```
Instruction:
```c
memmap_id = stack[TOP--];
addr = stack[TOP--];
size = stack[TOP--];
stack[++TOP] = __mem_write(memmap_id, addr, size);
```

#### map
Machine Code
```
62
```
Instruction:
```c
addr = stack[TOP--];
size = stack[TOP--];
stack[++TOP] = __mem_map(addr, size, flags);
```

#### unmap
Machine Code
```
63
```
Instruction:
```c
addr = stack[TOP--];
stack[++TOP] = __mem_map(addr);
```

#### exit
Machine Code
```
64
```
Instruction:
```c
status = stack[TOP--];
__vm_exit(status);
```

### Special Operation
#### NOP
Machine Code
# Documentation of SCSBX

## Design
### Basics
SCSBX is a Virtual Machine for SECCON Online 2020.
The architecture is based on a stack machine.
Every instruction is 1-byte except for PUSH.

### Stack Region
The stack bottom locates at **0xfffe0000**.
The initial size of the stack is 0x10000.

This region grows to lower address.
If it conflicts with other used region and cannot grow the stack, the program is killed by SIGSEGV.

### Code Region
The machine code is allocated at **0x200000000000**.
This region is read-only.

## Instructions
### Stack Operation
#### PUSH
Machine Code:
```
20 XX XX XX XX
```
Instruction:
```c
stack[++TOP] = 0xXXXXXXXX;
```

#### POP
Machine Code:
```
21
```
Instruction:
```c
TOP--;
```

#### DUP
Machine Code:
```
22
```
Instruction:
```c
a = stack[TOP--];
stack[++TOP] = stack[TOP - a];
```
This instruction causes exception if `stack[TOP-a]` is out of the alive stack.

#### XCHG
Machine Code:
```
23
```
Instruction:
```c
a = stack[TOP--];
tmp = stack[TOP];
stack[TOP] = stack[TOP - a];
stack[TOP - a] = tmp;
```
This instruction discards `stack[TOP]` if `stack[TOP-a]` is out of the alive stack.

#### LOAD
Machine Code:
```
24
```
Instruction:
```c
memmap_id = stack[TOP--];
ofs = stack[TOP];
stack[TOP] = *(long*)&memmap[memmap_id].addr[ofs];
```
This instruction causes SIGSEGV if the memory is invalid.

#### STORE8
Machine Code:
```
25
```
Instruction:
```c
memmap_id = stack[TOP--];
ofs = stack[TOP--];
*(char*)&memmap[memmap_id].addr[ofs] = (char)stack[TOP--];
```

#### STORE16
Machine Code:
```
26
```
Instruction:
```c
memmap_id = stack[TOP--];
ofs = stack[TOP--];
*(short*)&memmap[memmap_id].addr[ofs] = (short)stack[TOP--];
```

#### STORE32
Machine Code:
```
27
```
Instruction:
```c
memmap_id = stack[TOP--];
ofs = stack[TOP--];
*(int*)&memmap[memmap_id].addr[ofs] = (int)stack[TOP--];
```

### Branch Operation
#### JMP / RET
Machine Code:
```
30
```
Instruction:
```c
t = stack[TOP--];
PC = t;
```
This instruction causes SIGILL if the branch target is out of the program region.

#### JEQ
Machine Code:
```
31
```
Instruction:
```c
t = stack[TOP--];
f = stack[TOP--];
a = stack[TOP--];
b = stack[TOP--];
if (a == b) {
  PC = t;
} else {
  PC = f;
}
```
This instruction causes SIGILL if the branch target is out of the program region.

#### JGT
Machine Code:
```
32
```
Instruction:
```c
t = stack[TOP--];
f = stack[TOP--];
a = stack[TOP--];
b = stack[TOP--];
if (a > b) {
  PC = t;
} else {
  PC = f;
}
```
This instruction causes SIGILL if the branch target is out of the program region.

#### JGE
Machine Code:
```
33
```
Instruction:
```c
t = stack[TOP--];
f = stack[TOP--];
a = stack[TOP--];
b = stack[TOP--];
if (a > b) {
  PC = t;
} else {
  PC = f;
}
```
This instruction causes SIGILL if the branch target is out of the program region.

#### CALL
Machine Code:
```
34
```
Instruction:
```c
t = stack[TOP--];
stack[++TOP] = PC;
PC = f;
```
This instruction causes SIGILL if the branch target is out of the program region.

### Arithmetic Operation

#### ADD
Machine Code:
```
40
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] += a;
```
This instruction discards overflowed value.

#### SUB
Machine Code:
```
41
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] -= a;
```

#### MUL
Machine Code
```
42
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] *= a;
```

#### DIV
Machine Code
```
43
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] /= a;
```
This instruction causes SIGFPE if `a` is zero.

#### MOD
Machine Code
```
44
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] %= a;
```
This instruction causes SIGFPE if `a` is zero.

#### ABS
Machine Code
```
45
```
Instruction:
```c
stack[TOP] = stack[TOP] < 0 ? -stack[TOP] : stack[TOP];
```

#### NEG
Machine Code
```
46
```
Instruction:
```c
stack[TOP] = -stack[TOP];
```

#### POW
Machine Code
```
47
```
Instruction:
```c
a = (float)stack[TOP--];
stack[TOP] = pow(a, (float)stack[TOP]);
```

### Logical Operation
#### NOT
Machine Code
```
50
```
Instruction:
```c
stack[TOP] ^= 0xffffffff;
```

#### AND
Machine Code
```
51
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] &= a;
```

#### OR
Machine Code
```
52
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] |= a;
```

#### XOR
Machine Code
```
53
```
Instruction:
```c
a = stack[TOP--];
stack[TOP] ^= a;
```

#### SHL
Machine Code
```
54
```
Instruction:
```c
c = stack[TOP--];
stack[TOP] <<= c;
```

#### SHR
Machine Code
```
55
```
Instruction:
```c
c = stack[TOP--];
stack[TOP] >>= c;
```

### System Operation
#### read
Machine Code
```
60
```
Instruction:
```c
memmap_id = stack[TOP--];
addr = stack[TOP--];
size = stack[TOP--];
stack[++TOP] = __mem_read(memmap_id, addr, size);
```

#### write
Machine Code
```
61
```
Instruction:
```c
memmap_id = stack[TOP--];
addr = stack[TOP--];
size = stack[TOP--];
stack[++TOP] = __mem_write(memmap_id, addr, size);
```

#### map
Machine Code
```
62
```
Instruction:
```c
addr = stack[TOP--];
size = stack[TOP--];
flags = stack[TOP--];
stack[++TOP] = __mem_map(addr, size, flags);
```

#### unmap
Machine Code
```
63
```
Instruction:
```c
memmap_id = stack[TOP--];
stack[++TOP] = __mem_map(memmap_id);
```

#### exit
Machine Code
```
64
```
Instruction:
```c
status = stack[TOP--];
__vm_exit(status);
```

### Special Operation
#### NOP
Machine Code
```
70
```
Instruction:
```c
// Do nothing
```

#### SHOW
Machine Code
```
71
```
Instruction:
```c
// Show stack
```
Instruction:
```c
// Do nothing
```

#### SHOW
Machine Code
```
71
```
Instruction:
```c
// Show stack info
```
