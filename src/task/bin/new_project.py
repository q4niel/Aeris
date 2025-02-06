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
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    while not setDir(): pass
    while not setName(): pass

    os.mkdir(Globals.path)

    cfg:str = f"{Globals.path}/proj.lua"
    shutil.copy("res/proj.lua", cfg)

    with open(cfg, "r+") as file:
        content:str = file.read()
        file.seek(0)
        file.write(content.replace("__PROJECT_NAME__", Globals.name))
        file.truncate()

    return

if __name__ == "__main__": main()