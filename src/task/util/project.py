import os
import shutil
from typing import List
from . import path
from . import lua
from . import clang

class Globals:
    projDir:str = ""
    config:dict = []
    initializedSystems:List[str] = []

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

def checkVersion(engineCfg:dict) -> bool:
    eng:dict = engineCfg["AerisVersion"]
    proj:dict = Globals.config["AerisVersion"]

    success:bool = (
        (eng.major == proj.major)
    and (eng.minor == proj.minor)
    and (eng.patch == proj.patch)
    )

    if not success:
        print(f"Version Mismatch:")
        print(f"    Aeris: v{eng.major}.{eng.minor}.{eng.patch}")
        print(f"    {Globals.config["ProjectName"]}: v{proj.major}.{proj.minor}.{proj.patch}")

    return success

def createOut(parent:str, outSuffix:str) -> str:
    path.safeDir(parent)
    out:str = (
        f"{parent}/{Globals.config["ProjectName"]}_"
        f"v{Globals.config["ProjectVersion"].major}"
        f".{Globals.config["ProjectVersion"].minor}"
        f".{Globals.config["ProjectVersion"].patch}"
        f"{outSuffix}"
    )
    path.hardDir(out)
    return out

def getSystemLocation(system:str) -> str:
    return system.split(";", 1)[0]

def getSystemSignature(system:str) -> str:
    return system.split(";", 1)[1]

def initSystemFiles() -> bool:
    for system in (
        lua.makeList(Globals.config["Systems"].inits)
    +   lua.makeList(Globals.config["Systems"].procs)
    +   lua.makeList(Globals.config["Systems"].exits)
    ):
        if not ";" in system:
            print(f"proj.lua: Invalid System Reference '{system}'")
            print("    => relative_path/file;function")
            return False

        location:str = f"{Globals.projDir}/{getSystemLocation(system)}"
        signature:str = getSystemSignature(system)

        if not os.path.exists(location) or os.path.isdir(location):
            print(f"proj.lua: '{getSystemLocation(system)}' file could not be found, is it relative to 'proj.lua'?")
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
            file.write(content.replace(f"void {signature}()", f"#include <user_api.hpp>\nUSER_API void {signature}()"))
            file.truncate()
        
        Globals.initializedSystems.append(system)

    return True

def cleanupSystemFiles() -> None:
    for system in Globals.initializedSystems:
        location:str = getSystemLocation(f"{Globals.projDir}/{system}")
        os.remove(location)
        os.rename(f"{location}_", location)
    return

def compileSources(flags:List[str]) -> bool:
    sources:List[str] = lua.makeList(Globals.config["Sources"])

    for source in sources:
        src:str = f"{Globals.projDir}/{source}"

        if not os.path.exists(src) or os.path.isdir(src):
            print(f"proj.lua: '{source}' file could not be found, is it relative to 'proj.lua'?")
            return False

        if not src.endswith(".cpp"):
            print(f"proj.lua: '{source}' is not a valid C++ source file. It must end in '.cpp'")
            return False

    objsDir:str = f"{Globals.projDir}/objects"
    path.hardDir(objsDir)

    for source in sources:
        src:str = f"{Globals.projDir}/{source[:-4]}"
        dst:str = f"{objsDir}/{os.path.basename(source)[:-4]}"
        clang.compile(flags, src, dst)

    return True

def build(directorySuffix:str, binarySuffix:str, compilerFlags:List[str]) -> None:
    Globals.projDir:str = selectProject()
    Globals.config:dict = lua.parse(f"{Globals.projDir}/proj.lua")

    if not checkVersion(lua.parse(f"res/proj.lua")): return

    outDir:str = createOut(f"{Globals.projDir}/out", directorySuffix)

    if initSystemFiles():
        compileSources(compilerFlags)

    cleanupSystemFiles()
    return