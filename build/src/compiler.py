import os
from typing import Self

def isInstalled() -> bool:
    return (0 == os.system("clang --version"))

def compile(src:str, out:str) -> bool:
    return (0 == os.system(f"clang -c {src} -o {out}"))

class BinaryBuilder:
    def __init__(self) -> None:
        self.name:str = ""
        self.buildDir = ""
        self.appendedObjects:str = ""
        return

    def setBinName(self, name:str) -> Self:
        self.name = name
        return self

    def setBuildDirectory(self, path:str) -> Self:
        self.buildDir = path
        return self

    def addObject(self, obj:str) -> Self:
        if (os.path.exists(obj)):
            self.appendedObjects += f"{obj} "
        return self

    def build(self) -> bool:
        return (0 == os.system(f"clang {self.appendedObjects}-o {self.buildDir}/{self.name}"))