#include "commands.h"
#include <stdio.h>
#include <stdlib.h>
#include "../datagen/version.h"
#include "util/fio.h"

void invalidCmd() {
    printf("Invalid Usage - Use '--help' for more information\n");
}

void helpCmd() {
    printf("Available commands:\n    %s\n    %s\n    %s\n", HELP_CMD, VERSION_CMD, TRANSPILE_CMD);
}

void versionCmd() {
    printf("Aeris %i.%i.%i\n", MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION);
}

void transpileCmd(const char *input, const char *output) {
    int count = 0;
    char *array = NULL;
    if (!fio.parse(input, &count, &array)) {
        printf("Failed to parse file: %s\n", input);
        return;
    }

    free(array);
}