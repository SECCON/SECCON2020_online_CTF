#include "scsbx.hpp"

void SCSBX::__logic_not()
{
  u32 a = __stack_pop();
  __stack_push(~a);
}

void SCSBX::__logic_and()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a & b);
}

void SCSBX::__logic_or ()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a | b);
}

void SCSBX::__logic_xor()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a ^ b);
}

void SCSBX::__logic_shl()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a << b);
}

void SCSBX::__logic_shr()
{
  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a >> b);
}
