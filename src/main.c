#include "util/hello.h"
#include <stdlib.h>

int main() {
    hello();

#ifdef PLATFORM_LINUX
    system("read -n 1 -s -p \"Press any key to continue...\" && echo \"\n\"");
#endif

#ifdef PLATFORM_WINDOWS
    system("pause");
#endif

    return 0;
}