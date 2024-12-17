#include "../token.h"
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>

const char *tokenTypeToString(TokenType type) {
    #define CASE(TYPE, STRING) case TYPE: return STRING

    switch (type) {
        CASE(WHITESPACE, "WHITESPACE");
        CASE(SEMI_COLON, "SEMI_COLON");
        CASE(COMMA, "COMMA");
        CASE(PERIOD, "PERIOD");
        CASE(COLON, "COLON");
        CASE(OPEN_PARENTHESES, "OPEN_PARENTHESES"); CASE(CLOSE_PARENTHESES, "CLOSE_PARENTHESES");
        CASE(OPEN_CURLY, "OPEN_CURLY"); CASE(CLOSE_CURLY, "CLOSE_CURLY");
        CASE(OPEN_SQUARE, "OPEN_SQUARE"); CASE(CLOSE_SQUARE, "CLOSE_SQUARE");
        CASE(OPEN_ANGLE, "OPEN_ANGLE"); CASE(CLOSE_ANGLE, "CLOSE_ANGLE");

        CASE(SYMBOL, "SYMBOL");
        CASE(INTEGER, "INTEGER");
        CASE(ASSIGNMENT_OPERATOR, "ASSIGNMENT_OPERATOR");
        CASE(INT_LITERAL, "INT_LITERAL");

        default: return "Unknown TokenType!!!";
    }
}

bool tokenize (
    int *charc,
    char **charv,
    int *tokenc,
    Token **tokenv
) {
    #define NEW_TOKEN(TYPE)                                             \
        (*tokenv) = realloc((*tokenv), sizeof(Token) * ((*tokenc) + 1));  \
        (*tokenv)[(*tokenc)].type = TYPE;                               \
        (*tokenv)[(*tokenc)].data = NULL;                               \
        (*tokenc)++

    #define SEPARATOR_CASE(CHAR, TYPE)  \
    case CHAR:                          \
        NEW_TOKEN(TYPE);                \
        continue

    for (int i = 0; i < *charc; i++) {
        switch ((*charv)[i]) {
            SEPARATOR_CASE(' ', WHITESPACE);
            SEPARATOR_CASE(';', SEMI_COLON);
            SEPARATOR_CASE(',', COMMA);
            SEPARATOR_CASE('.', PERIOD);
            SEPARATOR_CASE(':', COLON);
            SEPARATOR_CASE('(', OPEN_PARENTHESES); SEPARATOR_CASE(')', CLOSE_PARENTHESES);
            SEPARATOR_CASE('{', OPEN_CURLY); SEPARATOR_CASE('}', CLOSE_CURLY);
            SEPARATOR_CASE('[', OPEN_SQUARE); SEPARATOR_CASE(']', CLOSE_SQUARE);
            SEPARATOR_CASE('<', OPEN_ANGLE); SEPARATOR_CASE('>', CLOSE_ANGLE);

            case 'i': {
                if (peak("int", &i, charv)) {
                    NEW_TOKEN(INTEGER);
                    continue;
                }
            }

            default: {
                if (!isSeparator((*charv)[i-1]) || !isalpha((*charv)[i])) continue;

                NEW_TOKEN(SYMBOL);

                int j = 0;
                while (isalpha((*charv)[i + j])) j++;

                (*tokenv)[(*tokenc) - 1].data = malloc(sizeof(char) * j);
                strncpy((*tokenv)[(*tokenc) - 1].data, (*charv) + i, i + j);
                ((char*)(*tokenv)[(*tokenc) - 1].data)[j] = '\0';

                i += j - 1;
                continue;
            }
        }
    }

    return true;
}

bool peak(char *desired, int *index, char **charv) {
    if (strncmp (
            desired,
            (*charv) + (*index),
            strlen(desired)
        )
    ||  !isSeparator(*((*charv) + (*index) - 1))
    ||  !isSeparator(*((*charv) + (*index) + strlen(desired)))
    ) {
        return false;
    }

    (*index) += strlen(desired) - 1;
    return true;
}

bool isSeparator(const char character) {
    switch (character) {
        case ' ':
        case ';':
        case ',':
        case '.':
        case ':':
        case '(': case ')':
        case '{': case '}':
        case '[': case ']':
        case '<': case '>':
            return true;

        default: return false;
    }
}