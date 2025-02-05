int main__() {
    return 0;
}

#ifdef PLATFORM_LINUX
int main(int argc, char **argv) {
    return main__();
}
#endif

#ifdef PLATFORM_WINDOWS
#include <windows.h>
#include <stdio.h>

int WinMain (
    HINSTANCE hInstance,
    HINSTANCE hPrevInstance,
    LPSTR lpCmdLine,
    int nShowCmd
) {
    #ifdef DEBUG
    if (!AllocConsole()) return 1;
    FILE *file = nullptr;
    if (freopen_s(&file, "CONOUT$", "w", stdout)) return 1;
    #endif

    return main__();
}
#endif