#pragma once

#ifdef BUILD_AERIS_API
    #ifdef PLATFORM_WINDOWS
        #define AERIS_API __declspec(dllexport)
    #endif
    #ifdef PLATFORM_LINUX
        #define AERIS_API __attribute__((visibility("default")))
    #endif
#else
    #ifdef PLATFORM_WINDOWS
        #define AERIS_API __declspec(dllimport)
    #endif
    #ifdef PLATFORM_LINUX
        #define AERIS_API
    #endif
#endif