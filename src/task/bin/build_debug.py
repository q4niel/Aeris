import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import project
from util import path
from util import platform

def main() -> None:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    
    plat:str = ""
    rpathSetting:str = ""
    match platform.get():
        case platform.Platform.WINDOWS:
            plat = "-DPLATFORM_WINDOWS"

        case platform.Platform.LINUX:
            plat = "-DPLATFORM_LINUX"
            rpathSetting = "-Wl,-rpath,\\$ORIGIN"

        case platform.Platform.OTHER:
            print("Unsupported OS!")
            return

    project.build (
        "_debug",
        "_d",
        [
            f"-I{os.getcwd()}/inc",
            f"-I{os.getcwd()}/res",
            plat,
            "-DBUILD_USER_API",
            "-DDEBUG"
        ],
        [
            rpathSetting
        ]
    )
    return

if __name__ == "__main__": main()