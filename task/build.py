import sys
import os
import tomllib
import shutil
from typing import TypedDict, List

class Data:
    projDir:str
    isDebug:bool
    toml:dict

    @staticmethod
    def init() -> None:
        Data.isDebug = (
            True if input (
                "Debug: 1\n"
                "Release: 2\n"
                ": "
            ) == "1"
            else False
        )

        Data.projDir = os.path.dirname (
            os.path.dirname (
                os.path.abspath(sys.argv[0])
            )
        )
        os.chdir(Data.projDir)

        with open(f"{Data.projDir}/task/build.toml", "rb") as toml:
            Data.toml = tomllib.load(toml)

        return

def getFlags() -> str:
    allFlags:str = ""

    for flag in (
        Data.toml["flags"]["debug"] if Data.isDebug else
        Data.toml["flags"]["release"]
    ): allFlags += f"{flag} "

    for flag in (
        Data.toml["flags"]["linux"] if os.name == "posix" else
        Data.toml["flags"]["windows"]
    ): allFlags += f"{flag} "

    return allFlags

def compilation() -> None:
    for srcEntry in Data.toml["srcEntries"]:
        for src in srcEntry["srcs"]:
            
            source:str = f"{Data.projDir}/{srcEntry["dir"]}/{src}.cpp"
            out:str = f"{Data.projDir}/tmp/{src}.o"
            os.system(f"clang++ {getFlags()} -c {source} -o {out}")
    return

def linking() -> None:
    allObjects:str = ""
    for srcEntry in Data.toml["srcEntries"]:
        for src in srcEntry["srcs"]:
            allObjects += f"{Data.projDir}/tmp/{src}.o "

    out:str = f"{Data.projDir}/{Data.toml["buildDir"]}/main"
    ext:str = "" if os.name == "posix" else ".exe"

    os.system(f"clang++ {allObjects} -o {out}{ext}")
    return

def main() -> None:
    Data.init()

    if not os.path.exists("tmp"):
        os.mkdir("tmp")

    if os.path.exists(Data.toml["buildDir"]):
        shutil.rmtree(Data.toml["buildDir"])
    os.mkdir(Data.toml["buildDir"])

    compilation()
    linking()

    if os.path.exists("tmp"):
        shutil.rmtree("tmp")

    return

if __name__ == "__main__": main()