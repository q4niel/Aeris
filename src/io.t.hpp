#pragma once
#include "io.hpp"
#include <iostream>

template<typename T, typename ...Args>
void io::write(T t, Args ...args) {
    std::cout << t;
    if constexpr (sizeof ...(Args) > 0) {
        write(args...);
    }
}

template<typename ...Args>
void io::print(Args ...args) {
    write(args...);
    newline(1);
}

template<typename ...Args>
void io::trace(Args ...args) {
    for (const auto &arg : {args...}) {
        write(arg);
        newline(1);
    }
}

void io::newline(unsigned int count = 1) {
    while (count --> 0) {
        std::cout << '\n';
    }
}