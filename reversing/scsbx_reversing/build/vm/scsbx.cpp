#include <iomanip>
#include <iostream>
#include "scsbx.hpp"

int SCSBX::exec()
{
  do {
    try {
      __cpu_exec(code[pc]);
    } catch(SandboxException e) {
      std::cerr << "***** SCSBX Crash Report *****" << std::endl;
      std::cerr << " Exception thrown: " << e << std::endl;
      std::cerr << " PC: "
                << std::hex
                << std::setfill('0') << std::setw(8)
                << pc << std::endl;
      std::cerr << "******************************" << std::endl;
      return -6;
    }
    pc++;
  } while(pc < code_size);

  return status;
}

void SCSBX::__cpu_exec(u8 instr)
{
  u32 val;

  switch(instr) {
    /* Memory Operation */
  case INS_PUSH:
    val = *(u32*)(&code[pc+1]);
    __stack_push(val);
    pc += 4;
    break;
  case INS_POP:
    __stack_pop();
    break;
  case INS_DUP:
    __stack_dup();
    break;
  case INS_XCHG:
    __stack_xchg();
    break;
  case INS_LOAD32:
    __mem_load32();
    break;
  case INS_LOAD64:
    __mem_load64();
    break;
  case INS_STORE8:
    __mem_store8();
    break;
  case INS_STORE16:
    __mem_store16();
    break;
  case INS_STORE32:
    __mem_store32();
    break;
  case INS_SHOW:
    __stack_show();
    break;

    /* Branch Operation */
  case INS_JMP:
    __branch_jmp();
    break;
  case INS_JEQ:
    __branch_jeq();
    break;
  case INS_JGT:
    __branch_jgt();
    break;
  case INS_JGE:
    __branch_jge();
    break;
  case INS_CALL:
    __branch_call();
    break;

    /* Arithmetic Operation */
  case INS_ADD:
    __arith_add();
    break;
  case INS_SUB:
    __arith_sub();
    break;
  case INS_MUL:
    __arith_mul();
    break;
  case INS_DIV:
    __arith_div();
    break;
  case INS_MOD:
    __arith_mod();
    break;

    /* Logic Operation */
  case INS_NOT:
    __logic_not();
    break;
  case INS_AND:
    __logic_and();
    break;
  case INS_OR:
    __logic_or();
    break;
  case INS_XOR:
    __logic_xor();
    break;
  case INS_SHL:
    __logic_shl();
    break;
  case INS_SHR:
    __logic_shr();
    break;

    /* System Operation */
  case INS_READ:
    __sys_read();
    break;
  case INS_WRITE:
    __sys_write();
    break;
  case INS_MAP:
    __sys_map();
    break;
  case INS_UNMAP:
    __sys_unmap();
    break;
  case INS_EXIT:
    __sys_exit();
    break;

  default:
    throw ILLEGAL_INSTRUCTION;
  }  
}

void SCSBX::__assert_address_valid(u64 address)
{
  for(auto itr = memmap.begin(); itr != memmap.end(); ++itr) {
    if ((itr->first <= address) && (address < itr->first + itr->second))
      return;
  }

  throw INVALID_ACCESS;
}

void SCSBX::__assert_range_valid(u64 address, u64 size)
{
  for(auto itr = memmap.begin(); itr != memmap.end(); ++itr) {
    if ((itr->first <= address) && (address + size < itr->first + itr->second)) {
      return;
    }
  }

  throw INVALID_ACCESS;
}

void SCSBX::__assert_resource_available(u64 address, u32 size)
{
  for(auto itr = memmap.begin(); itr != memmap.end(); ++itr) {
    if (((itr->first <= address) && (address < itr->first + itr->second))
        || ((itr->first <= address + size) && (address + size < itr->first + itr->second))) {
      throw INVALID_ACCESS;
    }
  }
}

SCSBX::SCSBX(u8 *_code, u32 _size)
{
  /* Initialize stack */
  stack = (u32*)mmap((void*)STACK_BASE, STACK_SIZE_INIT,
                     PROT_READ | PROT_WRITE,
                     MAP_ANONYMOUS | MAP_PRIVATE,
                     -1, 0);
  top = 0;
  capacity = STACK_SIZE_INIT / sizeof(u32);

  /* Initialize code */
  code_size = _size;
  code = (u8*)mmap((void*)CODE_BASE, (code_size + 0xfff) & ~0xfff,
                   PROT_READ | PROT_WRITE,
                   MAP_ANONYMOUS | MAP_PRIVATE,
                   -1, 0);
  pc = 0;
  memcpy(code, _code, code_size);
  mprotect(code, (code_size + 0xfff) & ~0xfff, PROT_READ);

  /* Initialize status code */
  status = 0;

  /* Guard page */
  memmap.push_back(std::make_pair((u64)STACK_BASE + (u64)STACK_SIZE_INIT,
                                  0x100000000 - (u64)STACK_BASE - (u64)STACK_SIZE_INIT));

  ASSERT_STACK_INIT;
  ASSERT_CODE_INIT;
}

SCSBX::~SCSBX()
{
  for(auto itr = memmap.begin(); itr != memmap.end(); ++itr) {
    munmap((void*)itr->first, ((u64)itr->second + 0xfff) & ~0xfff);
  }
  memmap.clear();
  munmap(stack, capacity * sizeof(u32));
  munmap(code, (code_size + 0xfff) & ~0xfff);
}
