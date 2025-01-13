#pragma once
#include "io.hpp"
#include <iostream>

template<typename T, typename ...Args>
void ars::write(T t, Args ...args) {
    std::cout << t;
    if constexpr (sizeof ...(Args) > 0) {
        write(args...);
    }
}

template<typename ...Args>
void ars::print(Args ...args) {
    write(args...);
    newline(1);
}

template<typename ...Args>
void ars::trace(Args ...args) {
    for (const auto &arg : {args...}) {
        write(arg);
        newline(1);
    }
}

void ars::newline(unsigned int count = 1) {
    while (count --> 0) {
        std::cout << '\n';
    }
}