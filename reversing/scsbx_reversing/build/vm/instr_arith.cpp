#include "scsbx.hpp"

void SCSBX::__arith_add()
{
  DEBUG("ADD");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a + b);
}

void SCSBX::__arith_sub()
{
  DEBUG("SUB");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a - b);
}

void SCSBX::__arith_mul()
{
  DEBUG("MUL");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a * b);
}

void SCSBX::__arith_div()
{
  DEBUG("DIV");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a / b);
}

void SCSBX::__arith_mod()
{
  DEBUG("MOD");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a % b);
}
