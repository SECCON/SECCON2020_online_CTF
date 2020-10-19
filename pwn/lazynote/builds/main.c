#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *ptr;

void readline(const char *msg, char *buf, int size)
{
  printf("%s", msg);
  if (fgets(buf, size, stdin) == NULL)
    exit(0);
}

int readint(const char *msg)
{
  char buf[16];
  readline(msg, buf, 15);
  return (unsigned int)atoi(buf);
}

int menu() {
  puts("1.🧾 / 2.✏️ / 3.🗑️ / 4.👀");
  return readint("> ");
}

void babyheap(void)
{
  int as, rs;

  switch(menu()) {
  case 1:
    if ((as = readint("alloc size: ")) <= 0) {
      puts("invalid size 🥺");
      return;
    }
    if ((rs = readint("read size: ")) <= 0) {
      puts("invalid size 🥺");
      return;
    }
    if ((ptr = (char*)calloc(sizeof(char), as)) == NULL) {
      puts("memory error 🥺");
      exit(1);
    }
    readline("data: ", ptr, as < rs ? as : rs);
    ptr[rs-1] = 0;
    break;
  case 2:
  case 3:
  case 4:
    puts("not implemented 😋");
    break;
  default:
    puts("invalid choice 🥺");
    break;
  }
}

int main(void)
{
  int i;
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
  alarm(300);
  puts("👶 < Hi.");
  for(i = 0; i < 4; i++) babyheap();
  puts("👴 < Bye.");
  return 0;
}
