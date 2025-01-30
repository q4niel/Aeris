from typing import List
from lupa import LuaRuntime

def parse(file:str) -> dict:
    if (file[-4:] == ".lua"):
        file = file[:-4]

    runtime = LuaRuntime(unpack_returned_tuples=True)
    
    with open(f"{file}.lua", "rb") as f:
        runtime.execute(f.read())

    return runtime.globals()

def makeList(data:dict) -> List:
    return [data[key] for key in sorted(data, key=int)]