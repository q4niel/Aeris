version = {
    major = 0,
    minor = 0,
    patch = 0
}

resources = {
    {src = "src/res/main__.hpp", dst = "res/main__.hpp"},
    {src = "src/res/main__.cpp", dst = "res/main__.cpp"},
}

includes = {
    "src/eng/aeris_api.hpp",
    "src/eng/core/print.hpp",
    "src/eng/core/print.t.hpp"
}

flags = {"-std=c++23"}

binaries = {
    {
        name = "Aeris" .. version.major .. "-Core",
        type = "shared",
        flags = {"-DBUILD_AERIS_API"},
        libraries = {},
        srcs = {"src/eng/core/print"}
    }
}