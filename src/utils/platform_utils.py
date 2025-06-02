import platform
from enum import Enum, auto

class Platform(Enum):
    LINUX = auto()
    MACOS = auto()
    UNKNOWN = auto()

class PlatformUtils:
    @staticmethod
    def get_current_platform() -> Platform:
        system = platform.system().lower()
        if system == "linux":
            return Platform.LINUX
        elif system == "darwin":
            return Platform.MACOS
        return Platform.UNKNOWN

    @staticmethod
    def is_linux() -> bool:
        return PlatformUtils.get_current_platform() == Platform.LINUX

    @staticmethod
    def is_macos() -> bool:
        return PlatformUtils.get_current_platform() == Platform.MACOS
