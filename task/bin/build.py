import sys
import os
import shutil
import re
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import path
from util import lua
from util import platform

class Globals:
    cfg:dict = lua.parse("task/cfg/build.lua")
    tmpDir:str = "tmp"
    outDir:str = f"out/{cfg["Directory"]}"

def compile(flags:List[str], src:str) -> None:
    allFlags:str = " ".join(f"{flag}" for flag in flags)
    os.system(f"clang++ {allFlags} -c {src}.cpp -o {Globals.tmpDir}/{os.path.basename(src)}.o")
    return

def link(name:str, type:str, objs:List[str]) -> None:
    allObjs = " ".join(f"{Globals.tmpDir}/{os.path.basename(obj)}.o" for obj in objs)

    match type:
        case "executable":
            ext:str = ".exe" if platform.get() == platform.Platform.WINDOWS else ""
            os.system(f"clang++ {allObjs} -o {Globals.tmpDir}/{bin["name"]}{ext}")
        case "shared":
            ext:str = ".dll" if platform.get() == platform.Platform.WINDOWS else ".so"
            os.system(f"clang++ -shared {allObjs} -o {Globals.tmpDir}/{name}{ext}")
        case _:
            print("Error: Unsupported binary type!")
    return

def buildBinaries() -> None:
    globalFlags:List[str] = lua.makeList(Globals.cfg["GlobalFlags"])
    platformFlags:List[str] = lua.makeList(Globals.cfg["WindowsFlags" if platform.get() == platform.Platform.WINDOWS else "LinuxFlags"])

    for bin in lua.makeList(Globals.cfg["Binaries"]):
        srcs:List[str] = lua.makeList(bin["srcs"])

        for src in srcs:
            compile(globalFlags + platformFlags + lua.makeList(bin["flags"]), src)
        link(bin["name"], bin["type"], srcs)

        for src in srcs:
            compile(globalFlags + platformFlags + lua.makeList(bin["flags"]) + ["-DDEBUG"], src)
        link(bin["name"] + "_d", bin["type"], srcs)

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
    for file in lua.makeList(Globals.cfg["Transfer"]):
        if (os.path.isdir(file["src"])):
            shutil.copytree(file["src"], f"{Globals.outDir}/{file["dst"]}")
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