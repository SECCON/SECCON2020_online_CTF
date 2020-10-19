#include "scsbx.hpp"

void SCSBX::__stack_push(u32 value)
{
  stack[++top] = value;
}

u32 SCSBX::__stack_pop()
{
  ASSERT_STACK_NOT_EMPTY;
  return stack[top--];
}

void SCSBX::__stack_dup()
{
  u32 ofs = __stack_pop();
  ASSERT_INDEX_IN_RANGE(ofs);

  __stack_push(stack[top - ofs]);
}

void SCSBX::__stack_xchg()
{
  u32 ofs = __stack_pop();
  ASSERT_INDEX_IN_RANGE(ofs);

  u32 a = stack[top - ofs];
  u32 b = __stack_pop();
  __stack_push(a);
  stack[top - ofs] = b;
}

void SCSBX::__mem_load32()
{
  u64 address = (u64)__stack_pop();
  __assert_address_valid(address);

  __stack_push(*(u32*)address);
}

void SCSBX::__mem_load64()
{
  u64 address = (u64)__stack_pop();
  __assert_address_valid(address);

  __stack_push(*(u32*)(address + 4));
  __stack_push(*(u32*)address);
}

void SCSBX::__mem_store8()
{
  u64 address = (u64)__stack_pop();
  __assert_address_valid(address);

  u8 value = (u8)__stack_pop();
  *(u8*)address = value;
}

void SCSBX::__mem_store16()
{
  u64 address = (u64)__stack_pop();
  __assert_address_valid(address);

  u16 value = (u16)__stack_pop();
  *(u16*)address = value;
}

void SCSBX::__mem_store32()
{
  u64 address = (u64)__stack_pop();
  __assert_address_valid(address);

  u32 value = (u32)__stack_pop();
  *(u32*)address = value;
}

void SCSBX::__stack_show()
{
  std::cout << "----- STACK TOP -----" << std::endl;
  for(int i = 0; i < 10; i++) {
    if (top - i == 0) {
      std::cout << "---------------------" << std::endl;
      return;
    }
    std::cout << i << " | " << std::hex << stack[top-i] << std::endl;
  }
  std::cout << ". |   ..." << std::endl;
  std::cout << "---------------------" << std::endl;
}
