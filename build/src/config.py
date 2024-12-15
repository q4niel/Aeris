import os
import tomllib
from typing import List

class Config:
    binaryName:str = ""
    sources:List[str] = []

    class Version:
        major:int = 0
        minor:int = 0
        patch:int = 0

    class Datagen:
        path:str = ""
        version:str = ""

    @staticmethod
    def loadToml(path:str) -> bool:
        if not (os.path.exists(path)): return False

        with open(path, "rb") as file:
            data:dict = tomllib.load(file)

            Config.binaryName = data["binaryName"]
            Config.sources = data["sources"]

            Config.Version.major = data["version"]["major"]
            Config.Version.minor = data["version"]["minor"]
            Config.Version.patch = data["version"]["patch"]

            Config.Datagen.path = data["datagen"]["path"]
            Config.Datagen.version = data["datagen"]["version"]

            return True
        return False