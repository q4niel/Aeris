#include "commands.h"
#include <stdio.h>
#include "../datagen/version.h"

void invalidCmd() {
    printf("Invalid Usage - Use '--help' for more information\n");
}

void helpCmd() {
    printf("Available commands:\n    %s\n    %s\n    %s\n", HELP_CMD, VERSION_CMD, TRANSPILE_CMD);
}

void versionCmd() {
    printf("Aeris %i.%i.%i\n", MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION);
}

void transpileCmd(const char **cmdv, bool output) {}