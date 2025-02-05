import os
import sys
import shutil

class Globals:
    dir:str = ""
    name:str = ""
    path:str = ""

def setDir() -> bool:
    Globals.dir = input("Directory: ")

    if not os.path.isabs(Globals.dir):
        print("Path is not absolute!")
        return False

    return True

def setName() -> bool:
    Globals.name = input("Name: ")
    Globals.path = f"{Globals.dir}/{Globals.name}"

    if os.path.exists(Globals.path):
        print("Path already exists!")
        return False

    return True

def main() -> None:
    while not setDir(): pass
    while not setName(): pass

    os.mkdir(Globals.path)

    cfgTemplate:str = f"{os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))}/res/proj.lua"
    cfg:str = f"{Globals.path}/proj.lua"

    shutil.copy(cfgTemplate, cfg)

    with open(cfg, "r+") as file:
        content:str = file.read()
        file.seek(0)
        file.write(content.replace("__NAME__", Globals.name))
        file.truncate()

    return

if __name__ == "__main__": main()