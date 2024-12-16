#include "../fio.h"
#include <stdlib.h>
#include <stdio.h>

static const bool parse(const char *path, int *count, char **array);

const FIO fio = {
    parse
};

static const bool parse(const char *path, int *count, char **array) {
    FILE *file = fopen(path, "r");
    if (file == NULL) return false;

    while (fgetc(file) != EOF) (*count)++;
    (*count)++;
    rewind(file);

    (*array) = malloc(sizeof(char) * (*count));
    if ((*array) == NULL) {
        fclose(file);
        return false;
    }

    for (int i = 0; i < *count; i++) {
        (*array)[i] = fgetc(file);
    }
    (*array)[*count] = '\0';

    fclose(file);
    return true;
}