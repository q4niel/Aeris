#pragma once
#include "print.hpp"
#include <iostream>

template<typename T, typename ...Args>
void ars__::print__(T t, Args ...args) {
    std::cout << t;
    if constexpr (sizeof ...(Args) > 0) {
        print__(args...);
    }
}

template<typename ...Args>
void ars__::println__(Args ...args) {
    print__(args...);
    printsep__(1);
}

template<typename ...Args>
void ars__::printlns__(Args ...args) {
    for (const auto &arg : {args...}) {
        print__(arg);
        printsep__(1);
    }
}

void ars__::printsep__(unsigned int count = 1) {
    while (count --> 0) {
        std::cout << '\n';
    }
}