#include "scsbx.hpp"

void SCSBX::__arith_add()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a + b);
}

void SCSBX::__arith_sub()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a - b);
}

void SCSBX::__arith_mul()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a * b);
}

void SCSBX::__arith_div()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a / b);
}

void SCSBX::__arith_mod()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a % b);
}
