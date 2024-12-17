#include "commands.h"
#include <stdio.h>
#include <stdlib.h>
#include "../datagen/version.h"
#include "util/fio.h"
#include "util/token.h"

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
    int charc = 0;
    char *charv = NULL;
    if (!fio.parse(input, &charc, &charv)) {
        printf("Failed to parse file: %s\n", input);
        return;
    }

    int tokenc = 0;
    Token *tokenv = NULL;
    if (!tokenize(&charc, &charv, &tokenc, &tokenv)) {
        printf("Failed to tokenize file: %s\n", input);
        return;
    }

    for (int i = 0; i < tokenc; i++) {
        printf (
            "%s %s\n",
            tokenTypeToString(tokenv[i].type),
            tokenv[i].type == SYMBOL ? (char*)tokenv[i].data : ""
        );
    }

    for (int i = 0; i < tokenc; i++) {
        switch (tokenv[i].type) {
            case SYMBOL:
            // case INT_LITERAL:
                free(tokenv[i].data);

            default: continue;
        }
    }
    free(tokenv);
    free(charv);
}