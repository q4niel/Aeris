import os
from . import platform
from enum import Enum, auto
from typing import List

class BinType(Enum):
    EXECUTABLE = auto()
    SHARED = auto()

def compile(flags:List[str], src:str, dst:str) -> None:
    allFlags:str = " ".join(f"{flag}" for flag in flags)
    os.system(f"clang++ {allFlags} -c {src}.cpp -o {dst}.o")
    return

def link(dst:str, type:BinType, objs:List[str]) -> None:
    allObjs = " ".join(f"{obj}.o" for obj in objs)

    match type:
        case BinType.EXECUTABLE:
            ext:str = ".exe" if platform.get() == platform.Platform.WINDOWS else ""
            os.system(f"clang++ {allObjs} -o {dst}{ext}")
        case BinType.SHARED:
            ext:str = ".dll" if platform.get() == platform.Platform.WINDOWS else ".so"
            os.system(f"clang++ -shared {allObjs} -o {dst}{ext}")
        case _:
            print("Error: Unsupported binary type!")
    return