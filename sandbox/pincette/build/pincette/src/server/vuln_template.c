#include <unistd.h>
void _start()
{
    struct{
        char a[8];
        int (*b)(const char*,char*const*,char*const*);
        char c[16];
    } st;
    st.b = execve;
    read(0, st.a, 32);
    st.b("/bin/sh", NULL, NULL);
}
