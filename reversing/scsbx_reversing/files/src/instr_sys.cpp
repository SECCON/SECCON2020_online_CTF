#include "scsbx.hpp"

void SCSBX::__sys_read()
{
  u64 address = (u64)__stack_pop();
  u32 size    = __stack_pop();
  __assert_range_valid(address, size);

  if (read(STDIN_FILENO, (void*)address, size) == 0)
    throw IO_ERROR;
}

void SCSBX::__sys_write()
{
  u64 address = (u64)__stack_pop();
  u32 size    = __stack_pop();
  __assert_range_valid(address, size);

  if (write(STDOUT_FILENO, (void*)address, size) == 0)
    throw IO_ERROR;
}

void SCSBX::__sys_map()
{
  u8 *p;
  u64 address = ((u64)__stack_pop()) & ~0xfff;
  u32 size    = __stack_pop();
  __assert_resource_available(address, size);

  p = (u8*)mmap((void*)address, ((u64)size + 0xfff) & ~0xfff,
                PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS,
                -1, 0);
  if (p == MAP_FAILED)
    throw MEMORY_ERROR;
  if ((u64)p != address) {
    munmap(p, ((u64)size + 0xfff) & ~0xfff);
    throw MEMORY_ERROR;
  }

  memmap.push_back(std::make_pair(address, size));
}

void SCSBX::__sys_unmap()
{
  u64 address = ((u64)__stack_pop()) & ~0xfff;
  __assert_address_valid(address);

  for(auto itr = memmap.begin(); itr != memmap.end(); ++itr) {
    if (address == itr->first) {
      memmap.erase(itr);
      munmap((void*)address, itr->second);
      return;
    }
  }

  throw MEMORY_ERROR;
}

void SCSBX::__sys_exit()
{
  u32 status_code = __stack_pop();
  status = (int)status_code;
  pc = code_size;
}
