#pragma once
#include <stdbool.h>

typedef struct FIO {
    const bool(*parse)(const char *, int *, char **);
} FIO;

extern const FIO fio;