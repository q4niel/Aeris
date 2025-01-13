#pragma once

#ifdef DEBUG
#define IMPLEMENTATION ;
#else
#define IMPLEMENTATION {}
#endif

namespace io {
    template<typename T, typename ...Args>
    void write(T t, Args ...args)IMPLEMENTATION

    template<typename ...Args>
    void print(Args ...args)IMPLEMENTATION

    template<typename ...Args>
    void trace(Args ...args)IMPLEMENTATION

    void newline(unsigned int count)IMPLEMENTATION
}

#ifdef DEBUG
#include "io.t.hpp"
#endif