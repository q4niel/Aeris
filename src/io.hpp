#pragma once

#ifdef DEBUG
#define NO_IMPL ;
#else
#define NO_IMPL {}
#endif

namespace ars {
    template<typename T, typename ...Args>
    void write(T t, Args ...args)NO_IMPL

    template<typename ...Args>
    void print(Args ...args)NO_IMPL

    template<typename ...Args>
    void trace(Args ...args)NO_IMPL

    void newline(unsigned int count)NO_IMPL
}

#ifdef DEBUG
#include "io.t.hpp"
#endif