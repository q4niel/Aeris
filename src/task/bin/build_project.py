import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import clang
from util import lua
from util import path

class Globals:
    projDir:str = ""
    cfg:dict = []
    outDir:str = ""

def selectProject(path:str) -> bool:
    if not os.path.isabs(path):
        print(f"'{path}' is not absolute!")
        return False

    if not os.path.exists(path):
        print(f"'{path}' does not exist!")
        return False

    if not os.path.exists(f"{path}/proj.lua"):
        print(f"'{path}' has no 'proj.lua' file, is '{path}' a valid Aeris Project?")
        return False

    Globals.projDir = path
    Globals.cfg = lua.parse(f"{path}/proj.lua")

    return True

def checkVersion() -> bool:
    eng:dict = lua.parse(f"res/proj.lua")["AerisVersion"]
    proj:dict = Globals.cfg["AerisVersion"]

    success:bool = (
        (eng.major == proj.major)
    and (eng.minor == proj.minor)
    and (eng.patch == proj.patch)
    )

    if not success:
        print(f"Version Mismatch:")
        print(f"    Aeris: v{eng.major}.{eng.minor}.{eng.patch}")
        print(f"    {Globals.cfg["Name"]}: v{proj.major}.{proj.minor}.{proj.patch}")

    return success

def createDirectories() -> None:
    path.safeDir(f"{Globals.projDir}/out")
    Globals.outDir = (
        f"{Globals.projDir}/out/{Globals.cfg["ProjectName"]}_"
        f"v{Globals.cfg["ProjectVersion"].major}"
        f".{Globals.cfg["ProjectVersion"].minor}"
        f".{Globals.cfg["ProjectVersion"].patch}"
    )
    path.hardDir(f"{Globals.outDir}")
    path.hardDir(f"{Globals.outDir}_debug")
    return

def build() -> bool:
    # for src in lua.makeList(cfg["Sources"]):
        # clang.compile()

    return True

def main() -> None:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    
    while not selectProject(input("Select Project: ")): pass
    if not checkVersion(): return

    createDirectories()

    if not build(): return

    return

if __name__ == "__main__": main()