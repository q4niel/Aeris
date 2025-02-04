import sys
import os
import shutil
import re
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import path
from util import lua

class Globals:
    platformFlag:str = ""
    executableExt:str = ""
    dynamicExt:str = ""
    staticExt:str = ""
    cfg:dict = []
    tmp:str = ""
    out:str = ""

def link(outSuffix:str, flags:List[str]) -> None:
    for bin in lua.makeList(Globals.cfg["binaries"]):
        allFlags = " ".join(f"{flag}" for flag in flags + lua.makeList(bin["flags"]))
        srcs = lua.makeList(bin["srcs"])

        for src in srcs:
            os.system(f"clang++ {allFlags} -c {src}.cpp -o {Globals.tmp}/{os.path.basename(src)}.o")

        allLibs = " ".join(f"{lib}{Globals.staticExt}" for lib in lua.makeList(bin["libraries"]))
        allObjs = " ".join(f"{Globals.tmp}/{os.path.basename(src)}.o" for src in srcs)

        match bin["type"]:
            case "shared":
                os.system(f"clang++ -shared {allLibs} {allObjs} -o {Globals.tmp}/{bin["name"]}{outSuffix}{Globals.dynamicExt}")
            case "executable":
                os.system(f"clang++ {allLibs} {allObjs} -o {Globals.tmp}/{bin["name"]}{outSuffix}{Globals.executableExt}")
            case _:
                print("Unsupported binary type")
    return

def main() -> None:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    match os.name:
        case "posix":
            Globals.platformFlag = "-DPLATFORM_LINUX"
            Globals.executableExt = ""
            Globals.dynamicExt = ".so"
            Globals.staticExt = ".a"
        case "nt":
            Globals.platformFlag = "-DPLATFORM_WINDOWS"
            Globals.executableExt = ".exe"
            Globals.dynamicExt = ".dll"
            Globals.staticExt = ".lib"
        case _:
            print("Unsupported OS")
            return

    Globals.cfg = lua.parse("task/cfg/build.lua")

    Globals.tmp = "tmp"
    Globals.out = f"out/aeris_v{Globals.cfg["version"]["major"]}.{Globals.cfg["version"]["minor"]}.{Globals.cfg["version"]["patch"]}"

    path.hardDir(Globals.tmp)
    path.safeDir("out")
    path.hardDir(Globals.out)
    path.hardDir(f"{Globals.out}/bin")
    path.hardDir(f"{Globals.out}/inc")
    path.hardDir(f"{Globals.out}/res")
    path.hardDir(f"{Globals.out}/task")

    for res in lua.makeList(Globals.cfg["transfer"]):
        if (os.path.isdir(res["src"])):
            shutil.copytree(res["src"], f"{Globals.out}/{res["dst"]}")
        else:
            shutil.copy(res["src"], f"{Globals.out}/{res["dst"]}")

    for inc in lua.makeList(Globals.cfg["includes"]):
        dst = f"{Globals.out}/inc/{os.path.basename(inc)}"
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

    flags = lua.makeList(Globals.cfg["flags"]) + [Globals.platformFlag]
    link("_d", flags + ["-DDEBUG"])
    link("", flags + ["-DRELEASE"])

    binaries:List[str] = []
    for root, dirs, bins in os.walk(Globals.tmp):
        for bin in bins:
            if bin.endswith(Globals.executableExt) or bin.endswith(Globals.dynamicExt) or bin.endswith(Globals.staticExt):
                binaries.append(bin)
    
    for bin in binaries:
        shutil.copy(f"{Globals.tmp}/{bin}", f"{Globals.out}/bin/{bin}")

    path.delDir(Globals.tmp)
    return

if __name__ == "__main__": main()