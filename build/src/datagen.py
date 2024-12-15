import sys
import os
import shutil
from config import Config
from typing import List

class Datagen:
    path:str = ""

    @staticmethod
    def init() -> None:
        Datagen.path = f"{sys.argv[2]}/{Config.Datagen.path}"

        if (os.path.exists(Datagen.path)):
            shutil.rmtree(Datagen.path)
        os.mkdir(Datagen.path)

        return

    @staticmethod
    def genHeader(name:str, defines:List[str] = []) -> None:
        with open(f"{Datagen.path}/{name}.h", "w") as file:
            file.write("#pragma once")
            for define in defines:
                file.write(f"\n#define {define}")
        return