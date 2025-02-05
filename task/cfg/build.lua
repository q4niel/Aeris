Version = {
    major = 0,
    minor = 0,
    patch = 0
}

Directory = "aeris_v" .. Version.major .. "." .. Version.minor .. "." .. Version.patch

Transfer = {
    {src = "src/res", dst = "res"},

    {src = "src/task/bin/build_project.py", dst = "task/bin/Build-Project"},
    {src = "src/task/bin/new_project.py", dst = "task/bin/New-Project"},

    {src = "task/util", dst = "task/util"},
    {src = "task/requirements.txt", dst = "task/requirements.txt"},
    {src = "task/run.bat", dst = "task/run.bat"},
    {src = "task/run.ps1", dst = "task/run.ps1"},
    {src = "task/run.sh", dst = "task/run.sh"}
}

Includes = {
    "src/eng/aeris_api.hpp",
    "src/eng/core/print.hpp",
    "src/eng/core/print.t.hpp"
}

GlobalFlags = {"-std=c++23"}
WindowsFlags = {"-DPLATFORM_WINDOWS"}
LinuxFlags = {"-DPLATFORM_LINUX"}

Binaries = {
    {
        name = "Aeris" .. Version.major .. "-Core",
        type = "shared",
        flags = {"-fvisibility=hidden", "-DBUILD_AERIS_API"},
        srcs = {"src/eng/core/print"}
    }
}