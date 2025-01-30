import os
import shutil

def hardDir(path:str) -> None:
    if (os.path.exists(path)):
        shutil.rmtree(path)
    os.mkdir(path)
    return

def safeDir(path:str) -> None:
    if not (os.path.exists(path)):
        os.mkdir(path)
    return

def delDir(path:str) -> None:
    if (os.path.exists(path)):
        shutil.rmtree(path)
    return