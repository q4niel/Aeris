version = {
    major = 0,
    minor = 0,
    patch = 0
}

directory = "aeris_v" .. version.major .. "." .. version.minor .. "." .. version.patch

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

globalFlags = {"-std=c++23"}
windowsFlags = {"-DPLATFORM_WINDOWS"}
linuxFlags = {"-DPLATFORM_LINUX"}

binaries = {
    {
        name = "Aeris" .. version.major .. "-Core",
        type = "shared",
        flags = {"-fvisibility=hidden", "-DBUILD_AERIS_API"},
        srcs = {"src/eng/core/print"}
    }
}