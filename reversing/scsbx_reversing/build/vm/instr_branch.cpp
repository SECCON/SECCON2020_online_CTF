#include "scsbx.hpp"

void SCSBX::__branch_jmp()
{
  DEBUG("JMP");

  pc = __stack_pop() - 1;
}

void SCSBX::__branch_jeq()
{
  DEBUG("JEQ");

  u32 t = __stack_pop() - 1;
  u32 f = __stack_pop() - 1;
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  pc = a == b ? t : f;
}

void SCSBX::__branch_jgt()
{
  DEBUG("JGT");

  u32 t = __stack_pop() - 1;
  u32 f = __stack_pop() - 1;
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  pc = a > b ? t : f;
}

void SCSBX::__branch_jge()
{
  DEBUG("JGE");

  u32 t = __stack_pop() - 1;
  u32 f = __stack_pop() - 1;
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  pc = a >= b ? t : f;
}

void SCSBX::__branch_call()
{
  DEBUG("CALL");

  u32 t = __stack_pop() - 1;
  __stack_push(pc + 1);
  pc = t;
}
