import os
from typing import List
from . import path

def selectProject() -> str:
    def select(path:str) -> bool:
        if not os.path.isabs(path):
            print(f"'{path}' is not absolute!")
            return False

        if not os.path.exists(path):
            print(f"'{path}' does not exist!")
            return False

        if not os.path.exists(f"{path}/proj.lua"):
            print(f"'{path}' has no 'proj.lua' file, is '{path}' a valid Aeris Project?")
            return False
        
        return True

    while not select(proj := input("Select Project: ")): pass
    return proj

def checkVersion(engineCfg:dict, projectCfg:dict) -> bool:
    eng:dict = engineCfg["AerisVersion"]
    proj:dict = projectCfg["AerisVersion"]

    success:bool = (
        (eng.major == proj.major)
    and (eng.minor == proj.minor)
    and (eng.patch == proj.patch)
    )

    if not success:
        print(f"Version Mismatch:")
        print(f"    Aeris: v{eng.major}.{eng.minor}.{eng.patch}")
        print(f"    {projectCfg["ProjectName"]}: v{proj.major}.{proj.minor}.{proj.patch}")

    return success

def createOut(parent:str, projectCfg:str, outSuffix:str) -> str:
    path.safeDir(parent)
    out:str = (
        f"{parent}/{projectCfg["ProjectName"]}_"
        f"v{projectCfg["ProjectVersion"].major}"
        f".{projectCfg["ProjectVersion"].minor}"
        f".{projectCfg["ProjectVersion"].patch}"
        f"{outSuffix}"
    )
    path.hardDir(out)
    return out

def build(directorySuffix:str, binarySuffix:str, binaryFlags:List[str]) -> None:
    projDir:str = selectProject()
    config:dict = lua.parse(f"{projDir}/proj.lua")

    if not checkVersion(lua.parse(f"res/proj.lua"), config): return

    outDir:str = createOut(f"{projDir}/out", config, directorySuffix)
    return

def buildRelease() -> None:
    build("", "", [])
    return

def buildDebug() -> None:
    build("_debug", "_d", ["-DDEBUG"])
    return