_start:
  ;; id = map(0xdead0000, 0x1000)
  push 0x1000
  push 0xdead0000
  sys_map

  push PutAnswer
  call
  push Finit
  call

  ;; copy "FLAG: "
  push 0x47414c46
  push 0xdead0004
  store32
  push 0x203a
  push 0xdead0008
  store16

  ;; write(0xdead0004, 0x6)
  push 0x6
  push 0xdead0004
  sys_write

  ;; read(0xdead000a, 0x40)
  push 0x40
  push 0xdead000a
  sys_read

  push 8                        ; i = 8
  push LpCmp1
  jmp
Lp1:
  push 0
  dup
  push 8
  sub
  push 8
  mul
  push 0
  dup
  push 0xdead000a
  add
  push 0
  dup
  load32                        ; A = *(u32*)&flag[(8-i)*8]
  push 0
  xchg
  push 2
  xchg
  push 0xdead000e
  add
  push 0
  dup
  push 3
  xchg
  push 1
  xchg
  load32                        ; B = *(u32*)&flag[(8-i)*8+4]

  push 3                        ; j = 3
  push LpCmp2
  jmp
Lp2:
  ;; Round
  push 2                        ; enter
  dup
  push 2
  dup

  push 0                        ; B' = F(B')
  dup
  push F
  call

  push 2                        ; A, B = B, A ^ B'
  dup
  xor
  push 4
  xchg
  pop
  push 4
  xchg

  pop                           ; leave
  pop

  push 1                        ; j--
  push 1
  xchg
  sub
LpCmp2:
  push 0                        ; if (j != 0) goto Lp2
  dup
  push 0
  push Lp2
  push LpBreak2
  jeq
LpBreak2:
  push 4                        ; update block
  xchg
  store32
  push 1
  xchg
  store32
  pop                           ; remove j

  push 1                        ; i--
  push 1
  xchg
  sub
LpCmp1:
  push 0                        ; if (i != 0) goto Lp1
  dup
  push 0
  push Lp1
  push LpBreak1
  jeq
LpBreak1:
  pop                           ; remove i

  ;; compare routine
  push 0                        ; r = 0
  push 8                        ; i = 8
  push LpCmp3
  jmp
Lp3:
  push 0                        ; r |= (a-A) | (b-B)
  dup
  push 1
  push 1
  xchg
  sub
  push 8
  mul
  push 0xdead000a
  add
  push 0
  dup
  push 0x40
  add
  load64
  push 2
  xchg
  load64
  push 2
  xchg
  sub
  push 2
  xchg
  sub
  or

  push 1
  xchg
  push 2
  xchg
  or
  push 1
  xchg

  push 1                        ; i--
  push 1
  xchg
  sub
LpCmp3:
  push 0                         ; if (i != 0) goto Lp2
  dup
  push 0
  push Lp3
  push LpBreak3
  jeq
LpBreak3:
  push Wrong
  push Correct
  jeq

Wrong:
  push 0x6e6f7257
  push 0xdead0000
  store32
  push 0x0a212167
  push 0xdead0004
  store32
  push 8
  push 0xdead0000
  sys_write
  push Bye
  jmp

Correct:
  push 0x72726f43
  push 0xdead0000
  store32
  push 0x0a746365
  push 0xdead0004
  store32
  push 8
  push 0xdead0000
  sys_write
  push Bye
  jmp

Bye:
  ;; exit(0)
  push 0
  sys_exit

Finit:
  push 0x06d35bcd
  push 0xdead0000
  store32
  jmp

F:
  push 0xdead0000               ; update key
  load32
  push 0x77f
  mul
  push 0x32a
  push 1
  xchg
  sub
  push 0x305eb3ea
  push 1
  xchg
  mod
  push 0
  dup
  push 0xdead0000
  store32

  push 2
  dup
  xor
  not
  push 2
  xchg
  pop

  jmp

PutAnswer:
  push 0x46761223
  push 0xdead004a
  store32
  push 0x54bea5c5
  push 0xdead004e
  store32
  push 0x7a22e8f6
  push 0xdead0052
  store32
  push 0x5db493c9
  push 0xdead0056
  store32
  push 0x055d175e
  push 0xdead005a
  store32
  push 0x022fcd33
  push 0xdead005e
  store32
  push 0x42c46be6
  push 0xdead0062
  store32
  push 0x6d10a0e8
  push 0xdead0066
  store32
  push 0x53f4c278
  push 0xdead006a
  store32
  push 0x7279ec2a
  push 0xdead006e
  store32
  push 0x5491fb39
  push 0xdead0072
  store32
  push 0x49ac421f
  push 0xdead0076
  store32
  push 0x49ab3a37
  push 0xdead007a
  store32
  push 0x47855812
  push 0xdead007e
  store32
  push 0x5718bb05
  push 0xdead0082
  store32
  push 0x0540fb5b
  push 0xdead0086
  store32
  jmp

  
