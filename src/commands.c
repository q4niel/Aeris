#include <stdio.h>
#include <string.h>
#include "commands.h"
#include "../datagen/version.h"

void evaluateCommands(const int cmdc, const char *cmdv[]) {
    for (int i = 0; i < cmdc; i++) {
        if (strcmp(cmdv[i], VERSION_CMD) == 0) echoVersion();
    }
}

void echoVersion() {
    printf("Aeris %i.%i.%i\n", MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION);
}