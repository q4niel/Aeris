import os
import shutil
from typing import List
from . import path
from . import lua

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

def insertUserApi(config:dict, projDir:str) -> bool:
    systems:List[str] = (
        lua.makeList(config["Systems"].inits)
    +   lua.makeList(config["Systems"].procs)
    +   lua.makeList(config["Systems"].exits)
    )

    for system in systems:
        if not ";" in system:
            print(f"proj.lua: Invalid System Reference '{system}'")
            print("    => relative_path/file;function")
            return False

        location:str = f"{projDir}/{system.split(";", 1)[0]}"
        signature:str = system.split(";", 1)[1]

        if not os.path.exists(location) or os.path.isdir(location):
            print(f"proj.lua: '{location}' file could not be found, is it relative to 'proj.lua'?")
            return False

        with open(location, "r") as file:
            content:str = file.read()
            found = content.find(signature)

            if found == -1:
                print(f"proj.lua: '{signature}' could not be found")
                return False

            if content[found - 5:found] != "void ":
                print(f"proj.lua: '{signature}' must return 'void'")
                print(f"    => void {signature}")
                return False

            if content[found+len(signature)] != "(" or content[found+1+len(signature)] != ")":
                print(f"proj.lua: '{signature}' shall take zero arguments")
                print(f"    => {signature}()")
                return False
        
        shutil.copy(f"{location}", f"{location}_")

        with open(location, "r+") as file:
            content:str = file.read()
            file.seek(0)
            file.write(content.replace(f"void {signature}()", f"USER_API void {signature}()"))
            file.truncate()

    return True

def build(directorySuffix:str, binarySuffix:str, binaryFlags:List[str]) -> None:
    projDir:str = selectProject()
    config:dict = lua.parse(f"{projDir}/proj.lua")

    if not checkVersion(lua.parse(f"res/proj.lua"), config): return

    outDir:str = createOut(f"{projDir}/out", config, directorySuffix)

    if not insertUserApi(config, projDir): return

    return

def buildRelease() -> None:
    build("", "", [])
    return

def buildDebug() -> None:
    build("_debug", "_d", ["-DDEBUG"])
    return