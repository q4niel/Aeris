version = {
    major = 0,
    minor = 0,
    patch = 0
}

resources = {
    {src = "src/main.hpp", dst = "src/main.hpp"},
    {src = "src/main.cpp", dst = "src/main.cpp"}
}

flags = {"-std=c++23"}

binaries = {
    {
        name = "aeris",
        type = "shared",
        flags = {"-DBUILD_AERIS_API"},
        libraries = {},
        srcs = {"src/core/print"}
    }
}