import os
import tomllib
from typing import List

class Config:
    binaryName:str = ""
    buildDataPath:str = ""
    sources:List[str] = []

    class Version:
        major:int = 0
        minor:int = 0
        patch:int = 0

    @staticmethod
    def loadToml(path:str) -> bool:
        if not (os.path.exists(path)): return False

        with open(path, "rb") as file:
            data:dict = tomllib.load(file)

            Config.binaryName = data["binaryName"]
            Config.buildDataPath = data["buildDataPath"]
            Config.sources = data["sources"]

            Config.Version.major = data["version"]["major"]
            Config.Version.minor = data["version"]["minor"]
            Config.Version.patch = data["version"]["patch"]

            return True
        return False