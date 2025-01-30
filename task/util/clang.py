import os
from typing import List

def compile(src:str, out:str, flags:List[str]) -> None:
    allFlags = " ".join(f"{flag}" for flag in flags)
    os.system(f"clang++ {allFlags} -c {src} -o {out}")
    return

def linkExec(out:str, srcs:List[str]) -> None:
    allSrcs = " ".join(f"{src}" for src in srcs)
    os.system(f"clang++ {allSrcs} -o {out}")
    return

def linkDyn(out:str, srcs:List[str]) -> None:
    allSrcs:str = " ".join(f"{src}" for src in srcs)
    os.system(f"clang++ -shared {allSrcs} -o {out}")
    os.remove(f"{out[:-4]}.exp")
    os.rename(f"{out[:-4]}.lib", f"{out[:-4]}dll.lib")
    return