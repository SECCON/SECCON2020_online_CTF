#include "scsbx.hpp"

void SCSBX::__logic_not()
{
  DEBUG("NOT");

  u32 a = __stack_pop();
  __stack_push(~a);
}

void SCSBX::__logic_and()
{
  DEBUG("AND");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a & b);
}

void SCSBX::__logic_or ()
{
  DEBUG("OR");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a | b);
}

void SCSBX::__logic_xor()
{
  DEBUG("XOR");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a ^ b);
}

void SCSBX::__logic_shl()
{
  DEBUG("SHL");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a << b);
}

void SCSBX::__logic_shr()
{
  DEBUG("SHR");

  u32 a = __stack_pop();
  u32 b = __stack_pop();
  __stack_push(a >> b);
}
