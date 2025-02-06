import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from util import project

def main() -> None:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    project.buildRelease()
    return

if __name__ == "__main__": main()