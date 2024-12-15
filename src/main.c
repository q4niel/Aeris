#include "commands.h"

int main(const int argc, const char *argv[]) {
    evaluateCommands(argc - 1, argv + 1);
    return 0;
}