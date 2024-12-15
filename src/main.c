#include <string.h>
#include "commands.h"

int main(const int argc, const char **argv) {
    const char **inputs = argv + 1;

    switch (argc - 1) {
        case 0: {
            helpCmd();
            break;
        }

        case 1: {
            if (strcmp(inputs[0], HELP_CMD) == 0) helpCmd();
            else if (strcmp(inputs[0], VERSION_CMD) == 0) versionCmd();
            else invalidCmd();
            break;
        }

        case 2: {
            if (strcmp(inputs[1], TRANSPILE_CMD) == 0) {
                transpileCmd(inputs, false);
            }
            else invalidCmd();
            break;
        }

        case 3: {
            if (strcmp(inputs[1], TRANSPILE_CMD) == 0) {
                transpileCmd(inputs, true);
            }
            else invalidCmd();
            break;
        }

        default: {
            invalidCmd();
            // for (int i = 0; i < cmdc; i++) {}
            break;
        }
    }

    return 0;
}