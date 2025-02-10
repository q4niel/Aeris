import sys
import os
import shutil
import re
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import clang
from util import lua
from util import path
from util import platform

class Globals:
    cfg:dict = lua.parse("task/cfg/build.lua")
    tmpDir:str = "tmp"
    outDir:str = f"out/{cfg["Directory"]}"

def buildBinaries() -> None:
    globalFlags:List[str] = lua.makeList(Globals.cfg["GlobalFlags"])
    platformFlags:List[str] = lua.makeList(Globals.cfg["WindowsFlags" if platform.get() == platform.Platform.WINDOWS else "LinuxFlags"])

    for bin in lua.makeList(Globals.cfg["Binaries"]):
        srcs:List[str] = lua.makeList(bin["srcs"])
        objs:List[str] = []
        for src in srcs:
            objs.append(f"{Globals.tmpDir}/{os.path.basename(src)}")

        type:clang.BinType = clang.BinType.EXECUTABLE if bin["type"] == "executable" else clang.BinType.SHARED

        for src in srcs:
            clang.compile(globalFlags + platformFlags + lua.makeList(bin["flags"]), src, f"{Globals.tmpDir}/{os.path.basename(src)}")
        clang.link(f"{Globals.tmpDir}/{bin["name"]}", type, [], [], objs)

        for src in srcs:
            clang.compile(globalFlags + platformFlags + lua.makeList(bin["flags"]) + ["-DDEBUG"], src, f"{Globals.tmpDir}/{os.path.basename(src)}")
        clang.link(f"{Globals.tmpDir}/{bin["name"] + "_d"}", type, [], [], objs)

    return

def createDirectories() -> None:
    path.hardDir(Globals.tmpDir)
    path.safeDir("out")
    path.hardDir(Globals.outDir)
    path.hardDir(f"{Globals.outDir}/bin")
    path.hardDir(f"{Globals.outDir}/inc")
    path.hardDir(f"{Globals.outDir}/task")
    path.hardDir(f"{Globals.outDir}/task/bin")
    return

def transferFiles() -> None:
    def merge(src, dst) -> None:
        if not os.path.exists(dst):
            shutil.copytree(src, dst)
        else:
            for item in os.listdir(src):
                srcPath:str = os.path.join(src, item)
                dstPath:str = os.path.join(dst, item)

                if os.path.isdir(srcPath):
                    merge(srcPath, dstPath)
                else:
                    shutil.copy(srcPath, dstPath)
        return

    for file in lua.makeList(Globals.cfg["Transfer"]):
        if (os.path.isdir(file["src"])):
            merge(file["src"], f"{Globals.outDir}/{file["dst"]}")
        else:
            shutil.copy(file["src"], f"{Globals.outDir}/{file["dst"]}")
    return

def transferIncludes() -> None:
    for inc in lua.makeList(Globals.cfg["Includes"]):
        dst = f"{Globals.outDir}/inc/{os.path.basename(inc)}"
        shutil.copy(inc, dst)

        def replace(match) -> str:
            return f'#include "{os.path.basename(match.group(2))}"'

        with open(dst, 'r+') as file:
            content:str = file.read()
            file.seek(0)

            file.write(re.sub (
                r'(#include\s+"([^"]+)")',
                replace,
                content
            ))
            file.truncate()
    return

def transferBinaries() -> None:
    names:List[str] = []
    for bin in lua.makeList(Globals.cfg["Binaries"]):
        names.append(bin["name"])
        names.append(bin["name"] + "_d")

    for root, dirs, bins in os.walk(Globals.tmpDir):
        for bin in bins:
            if bin.split('.')[0] in names:
                shutil.copy(f"{root}/{bin}", f"{Globals.outDir}/bin/{bin}")

    return

def main() -> None:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    if (platform.get() == platform.Platform.OTHER):
        print("Error: Unsupported OS!")
        return

    createDirectories()
    buildBinaries()
    transferFiles()
    transferIncludes()
    transferBinaries()

    path.delDir(Globals.tmpDir)
    return

if __name__ == "__main__": main()