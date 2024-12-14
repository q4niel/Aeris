import sys
import os
from config import Config
import compiler
import shutil

def main() -> None:
    if not (Config.loadToml(f"{sys.argv[1]}/build/.toml")):
        print(f"error while loading data from {sys.argv[1]}/build/.toml")
        return


    tmpDir:str = f"{sys.argv[1]}/build/tmp"
    srcDir:str = f"{sys.argv[1]}/src"
    outDir:str = f"{sys.argv[1]}/build/out"

    os.mkdir(tmpDir)

    if (os.path.exists(outDir)):
        shutil.rmtree(outDir)
    os.mkdir(outDir)

    for src in Config.sources:
        if not (compiler.compile(f"{srcDir}/{src}.c", f"{tmpDir}/{os.path.basename(src)}.o")):
            print(f"error while compiling {srcDir}/{src}.c")

    builder = compiler.BinaryBuilder()

    for src in Config.sources:
        builder.addObject(f"{tmpDir}/{os.path.basename(src)}.o")

    (
        builder
        .setBinName(Config.binaryName)
        .setBuildDirectory(f"{sys.argv[1]}/build/out")
        .build()
    )

    shutil.rmtree(tmpDir)
    return

if __name__ == "__main__": main()