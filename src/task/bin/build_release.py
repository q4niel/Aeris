import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import project
from util import path

def main() -> None:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    path.hardDir("tmp")
    project.buildRelease()
    path.delDir("tmp")
    return

if __name__ == "__main__": main()