import os
import shutil
from typing import List
from . import path
from . import lua
from . import clang

class Globals:
    projDir:str = ""
    outDir:str = ""
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

def cleanup() -> None:
    for system in Globals.initializedSystems:
        location:str = getSystemLocation(f"{Globals.projDir}/{system}")
        os.remove(location)
        os.rename(f"{location}_", location)

    path.delDir(f"{Globals.outDir}/objects")
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

    objsDir:str = f"{Globals.outDir}/objects"
    path.hardDir(objsDir)

    clang.compile(flags, "res/main__", f"{objsDir}/main__")

    for source in sources:
        src:str = f"{Globals.projDir}/{source[:-4]}"
        dst:str = f"{objsDir}/{os.path.basename(source)[:-4]}"
        clang.compile(flags, src, dst)

    return True

def linkBinary(flags:List[str], libs:List[str]) -> bool:
    prevCWD:str = os.getcwd()

    path.hardDir(f"{Globals.outDir}/bin")
    os.chdir("bin")

    objects:List[str] = []
    for object in os.listdir(f"{Globals.outDir}/objects"):
        objects.append(f"{Globals.outDir}/objects/{object[:-2]}")

    clang.link(f"{Globals.outDir}/bin/{Globals.config["ExecutableName"]}", clang.BinType.EXECUTABLE, flags, libs, objects)

    os.chdir(prevCWD)
    return True

def build(directorySuffix:str, binarySuffix:str, compileFlags:List[str], linkFlags:List[str]) -> None:
    Globals.projDir = selectProject()
    Globals.config = lua.parse(f"{Globals.projDir}/proj.lua")
    Globals.outDir = createOut(f"{Globals.projDir}/out", directorySuffix)

    if not checkVersion(lua.parse(f"res/proj.lua")): return

    if (
        not initSystemFiles()
    or  not compileSources(compileFlags)
    or  not linkBinary(linkFlags, ["Aeris0-Core"])
    ):
        shutil.rmtree(Globals.outDir)

    cleanup()
    return