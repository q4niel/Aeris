import sys
import os
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from util import clang

def main() -> None:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    tmpDir:str = "task/buildTMP"

    if (os.path.exists(tmpDir)):
        shutil.rmtree(tmpDir)
    os.mkdir(tmpDir)

    clang.compile("src/core/print.cpp", f"{tmpDir}/print.o", ["-std=c++23", "-DBUILD_AERIS_API", "-DPLATFORM_WINDOWS", "-DDEBUG"])
    clang.linkDyn(f"core.dll", [f"{tmpDir}/print.o"])

    clang.compile("src/main.cpp", f"{tmpDir}/main.o", ["-std=c++23", "-DPLATFORM_WINDOWS", "-DDEBUG"])
    clang.linkExec("test.exe", [f"coredll.lib", f"{tmpDir}/main.o"])

    shutil.rmtree(tmpDir)
    return

if __name__ == "__main__": main()