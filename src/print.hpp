#pragma once

namespace ars__ {
    template<typename T, typename ...Args>
    void print__(T t, Args ...args);

    template<typename ...Args>
    void println__(Args ...args);

    template<typename ...Args>
    void printlns__(Args ...args);

    void printsep__(unsigned int count);
}

#include "print.t.hpp"