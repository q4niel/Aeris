import os
from enum import Enum, auto

class Platform(Enum):
    WINDOWS = auto()
    LINUX = auto()
    OTHER = auto()

def get() -> Platform:
    match os.name:
        case "nt": return Platform.WINDOWS
        case "posix": return Platform.LINUX
        case _: return Platform.OTHER