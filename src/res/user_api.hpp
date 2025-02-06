#pragma once

#ifdef BUILD_USER_API
    #ifdef PLATFORM_WINDOWS
        #define USER_API __declspec(dllexport)
    #endif
    #ifdef PLATFORM_LINUX
        #define USER_API __attribute__((visibility("default")))
    #endif
#else
    #ifdef PLATFORM_WINDOWS
        #define USER_API __declspec(dllimport)
    #endif
    #ifdef PLATFORM_LINUX
        #define USER_API
    #endif
#endif