#ifndef __SCSBX_HPP__
#define __SCSBX_HPP__

#include <vector>
#include <utility>
#include <iostream>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

#define STACK_BASE ((void*)0xfffe0000)
#define CODE_BASE  ((void*)0x55540000)
#define STACK_SIZE_INIT ((u32)0x10000)

typedef unsigned char  u8;
typedef unsigned short u16;
typedef unsigned int   u32;
typedef unsigned long  u64;
typedef std::string    str;

class SCSBX {
private:
  /* fields */
  std::vector<std::pair<u64, u32>> memmap;

  u32 pc;
  int status;

  u8* code;
  u32* stack;
  u32 code_size;
  u32 capacity;
  u32 top;

  void __cpu_exec (u8 instr);

  /* Memory Operations */
#define INS_PUSH    0x20
#define INS_POP     0x21
#define INS_DUP     0x22
#define INS_XCHG    0x23
#define INS_LOAD32  0x24
#define INS_LOAD64  0x25
#define INS_STORE8  0x26
#define INS_STORE16 0x27
#define INS_STORE32 0x28
#define INS_SHOW    0x70
  void __stack_push (u32 value);
  u32  __stack_pop  ();
  void __stack_dup  ();
  void __stack_xchg ();
  void __mem_load32 ();
  void __mem_load64 ();
  void __mem_store8 ();
  void __mem_store16();
  void __mem_store32();
  void __stack_show ();

  /* Branch Operations */
#define INS_JMP   0x30
#define INS_JEQ   0x31
#define INS_JGT   0x32
#define INS_JGE   0x33
#define INS_CALL  0x34
  void __branch_jmp ();
  void __branch_jeq ();
  void __branch_jgt ();
  void __branch_jge ();
  void __branch_call();

  /* Arithmetic Operations */
#define INS_ADD   0x40
#define INS_SUB   0x41
#define INS_MUL   0x42
#define INS_DIV   0x43
#define INS_MOD   0x44
  void __arith_add();
  void __arith_sub();
  void __arith_mul();
  void __arith_div();
  void __arith_mod();

  /* Logical Operations */
#define INS_NOT   0x50
#define INS_AND   0x51
#define INS_OR    0x52
#define INS_XOR   0x53
#define INS_SHL   0x54
#define INS_SHR   0x55
#define INS_ROL   0x56
#define INS_ROR   0x57
  void __logic_not();
  void __logic_and();
  void __logic_or ();
  void __logic_xor();
  void __logic_shl();
  void __logic_shr();

  /* System Operations */
#define INS_READ  0x60
#define INS_WRITE 0x61
#define INS_MAP   0x62
#define INS_UNMAP 0x63
#define INS_EXIT  0x64
  void __sys_map  ();
  void __sys_unmap();
  void __sys_read ();
  void __sys_write();
  void __sys_exit ();

  virtual void __assert_address_valid(u64 address);
  virtual void __assert_range_valid(u64 address, u64 size);
  virtual void __assert_resource_available(u64 address, u32 size);

public:
  SCSBX(u8 *code, u32 size);
  ~SCSBX();
  int exec();
};

enum SandboxException {
  MEMORY_ERROR,         // map fails
  IO_ERROR,             // I/O error
  UNINITIALIZED_STACK,  // stack is not initialized
  UNINITIALIZED_CODE,   // machine code is not initialized
  EMPTY_STACK,          // pop from empty stack
  STACK_OUT_OF_BOUNDS,  // trying to use a value out of stack region
  INVALID_ACCESS,       // invalid memory address
  ILLEGAL_INSTRUCTION,  // unknown instruction
};

#define ASSERT_STACK_INIT                       \
  if (stack == MAP_FAILED)                      \
    throw UNINITIALIZED_STACK;

#define ASSERT_STACK_NOT_EMPTY                  \
  if (top == 0)                                 \
    throw EMPTY_STACK;

#define ASSERT_CODE_INIT                        \
  if (code == MAP_FAILED)                       \
    throw UNINITIALIZED_CODE;

#define ASSERT_INDEX_IN_RANGE(ofs)              \
  if (top <= ofs)                               \
    throw STACK_OUT_OF_BOUNDS;

#endif
