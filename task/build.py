import sys
import os
import tomllib
import shutil
from typing import TypedDict, List

class Globals:
    projDir:str
    isDebug:bool
    data:dict

    @staticmethod
    def init() -> None:
        Globals.isDebug = (
            True if input (
                "Debug: 1\n"
                "Release: 2\n"
                ": "
            ) == "1"
            else False
        )

        Globals.projDir = os.path.dirname (
            os.path.dirname (
                os.path.abspath(sys.argv[0])
            )
        )

        with open(f"{Globals.projDir}/task/build.toml", "rb") as toml:
            Globals.data = tomllib.load(toml)

        return

def getFlags() -> str:
    allFlags:str = ""

    for flag in (
        Globals.data["flags"]["debug"] if Globals.isDebug else
        Globals.data["flags"]["release"]
    ): allFlags += f"{flag} "

    for flag in (
        Globals.data["flags"]["linux"] if os.name == "posix" else
        Globals.data["flags"]["windows"]
    ): allFlags += f"{flag} "

    return allFlags

def compilation() -> None:
    for srcEntry in Globals.data["srcEntries"]:
        for src in srcEntry["srcs"]:
            
            source:str = f"{Globals.projDir}/{srcEntry["dir"]}/{src}.cpp"
            out:str = f"{Globals.projDir}/tmp/{src}.o"
            os.system(f"clang++ {getFlags()} -c {source} -o {out}")
    return

def main() -> None:
    Globals.init()

    os.chdir(Globals.projDir)
    if not os.path.exists("tmp"): os.mkdir("tmp")

    compilation()

    if os.path.exists("tmp"): shutil.rmtree("tmp")
    return

if __name__ == "__main__": main()