#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "scsbx.hpp"

void myread(const char *msg, char *buf, int size)
{
  int s;
  s = write(1, msg, strlen(msg));
  if ((s = read(0, buf, size)) <= 0) _exit(0);
  buf[s] = '\0';
}

int readint(const char *msg)
{
  char buf[16] = {0};
  myread(msg, buf, 15);
  return atoi(buf);
}

int main(int argc, char **argv)
{
  unsigned int size;
  unsigned char *code;

  alarm(60);

  if (argc >= 2) {
    struct stat stbuf;
    int fd = open(argv[1], O_RDONLY);
    fstat(fd, &stbuf);
    size = stbuf.st_size;
    code = (unsigned char*)malloc(size);
    if (read(fd, code, size) != size) _exit(0);
    close(fd);
  } else {
    size = (unsigned int)readint("size: ");
    if (size > 0x1000) {
      write(2, "Too big\n", 8);
      _exit(0);
    }
    code = (unsigned char*)malloc(size);
    myread("code: ", (char*)code, size);
  }

  void *mem = mmap((void*)0x100000000, 0x1000, PROT_READ | PROT_WRITE,
                   MAP_PRIVATE | MAP_POPULATE | MAP_ANONYMOUS, -1, 0);
  SCSBX *sbx = new (mem) SCSBX(code, size);
  sbx->exec();
  munmap(mem, 0x1000);
  return 0;
}
