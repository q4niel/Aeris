import sys
import os
from config import Config
from platform import OS
import compiler
import shutil

def main() -> None:
    projDir:str = sys.argv[2]

    if not (Config.loadToml(f"{projDir}/build/.toml")):
        print(f"error while loading data from {projDir}/build/.toml")
        return


    tmpDir:str = f"{projDir}/build/tmp"
    srcDir:str = f"{projDir}/src"
    outDir:str = f"{projDir}/build/out"

    os.mkdir(tmpDir)

    if (os.path.exists(outDir)):
        shutil.rmtree(outDir)
    os.mkdir(outDir)

    platformDefine:str = ""
    match int(sys.argv[1]):
        case OS.LINUX.value:
            platformDefine = "PLATFORM_LINUX"
        case OS.WINDOWS.value:
            platformDefine = "PLATFORM_WINDOWS"
        case _:
            platformDefine = "PLATFORM_UNKNOWN"

    for src in Config.sources:
        if not (compiler.compile(f"{srcDir}/{src}.c", f"{tmpDir}/{os.path.basename(src)}.o", [platformDefine])):
            print(f"error while compiling {srcDir}/{src}.c")

    builder = compiler.BinaryBuilder()

    for src in Config.sources:
        builder.addObject(f"{tmpDir}/{os.path.basename(src)}.o")

    (
        builder
        .setBinName(Config.binaryName)
        .setBuildDirectory(f"{projDir}/build/out")
        .build()
    )

    shutil.rmtree(tmpDir)
    return

if __name__ == "__main__": main()