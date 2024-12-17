#pragma once
#include <stdbool.h>

typedef enum TokenType {
    WHITESPACE,
    SEMI_COLON,
    COMMA,
    PERIOD,
    COLON,
    OPEN_PARENTHESES, CLOSE_PARENTHESES,
    OPEN_CURLY, CLOSE_CURLY,
    OPEN_SQUARE, CLOSE_SQUARE,
    OPEN_ANGLE, CLOSE_ANGLE,

    SYMBOL,
    INTEGER,
    ASSIGNMENT_OPERATOR,
    INT_LITERAL
} TokenType;

const char *tokenTypeToString(TokenType type);

typedef struct Token {
    TokenType type;
    void *data;
} Token;

bool tokenize (
    int *charc,
    char **charv,
    int *tokenc,
    Token **tokenv
);

bool peak(char *desired, int *index, char **charv);
bool isSeparator(const char character);