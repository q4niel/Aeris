version = {
    major = 0,
    minor = 0,
    patch = 0
}

transfer = {
    {src = "src/res", dst = "res"},

    {src = "src/task/bin/new_project.py", dst = "task/bin/New-Project"},

    {src = "task/util", dst = "task/util"},
    {src = "task/requirements.txt", dst = "task/requirements.txt"},
    {src = "task/run.bat", dst = "task/run.bat"},
    {src = "task/run.ps1", dst = "task/run.ps1"},
    {src = "task/run.sh", dst = "task/run.sh"}
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
        flags = {"-fvisibility=hidden", "-DBUILD_AERIS_API"},
        libraries = {},
        srcs = {"src/eng/core/print"}
    }
}