#pragma once
#include <stdbool.h>

void invalidCmd();

#define HELP_CMD "--help"
void helpCmd();

#define VERSION_CMD "--version"
void versionCmd();

#define TRANSPILE_CMD "--transpile"
void transpileCmd(const char *input, const char *output);