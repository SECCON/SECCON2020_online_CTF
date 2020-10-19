#include "scsbx.hpp"

void SCSBX::__branch_jmp()
{
  pc = __stack_pop() - 1;
}

void SCSBX::__branch_jeq()
{
  u32 t = __stack_pop() - 1;
  u32 f = __stack_pop() - 1;
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  pc = a == b ? t : f;
}

void SCSBX::__branch_jgt()
{
  u32 t = __stack_pop() - 1;
  u32 f = __stack_pop() - 1;
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  pc = a > b ? t : f;
}

void SCSBX::__branch_jge()
{
  u32 t = __stack_pop() - 1;
  u32 f = __stack_pop() - 1;
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  pc = a >= b ? t : f;
}

void SCSBX::__branch_call()
{
  u32 t = __stack_pop() - 1;
  __stack_push(pc + 1);
  pc = t;
}
