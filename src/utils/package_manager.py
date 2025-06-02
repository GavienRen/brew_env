import platform
from abc import ABC, abstractmethod
from typing import List
from .shell import Shell
from .logger import log_info, log_error

class PackageManager(ABC):
    def __init__(self):
        self.shell = Shell()

    @abstractmethod
    def install(self, package: str) -> bool:
        pass

    @abstractmethod
    def update(self) -> bool:
        pass
    
    def batch_install(self, packages: List[str]) -> bool:
        return self._batch_install(packages)
    
    @abstractmethod
    def _batch_install(self, packages: List[str]) -> bool:
        pass

class AptManager(PackageManager):
    def install(self, package: str) -> bool:
        code, stdout, stderr = self.shell.run_sudo(f"apt install -y {package}")
        if code != 0:
            log_error(f"安装错误: {stderr}")
        return code == 0

    def update(self) -> bool:
        log_info("📦 更新APT软件包列表")
        code, stdout, stderr = self.shell.run_sudo("apt update")
        if code != 0:
            log_error(f"更新错误: {stderr}")
        log_info("更新APT软件包列表完成")
        return code == 0

    def _batch_install(self, packages: List[str]) -> bool:
        packages_str = " ".join(packages)
        log_info(f"📥 批量安装: {packages_str}")
        code, stdout, stderr = self.shell.run_sudo(f"apt install -y {packages_str}")
        if code != 0:
            log_error(f"批量安装错误: {stderr}")
        return code == 0

class BrewManager(PackageManager):
    def install(self, package: str) -> bool:
        _, _, stderr = self.shell.run(f"brew install {package}")
        return not stderr

    def update(self) -> bool:
        log_info("更新软件包列表")
        code, stdout, stderr = self.shell.run("brew update")
        if code != 0:
            log_error(f"更新错误: {stderr}")
        log_info("更新软件包列表完成")
        return code == 0

    def _batch_install(self, packages: List[str]) -> bool:
        packages_str = " ".join(packages)
        log_info(f"批量安装: {packages_str}")
        code, stdout, stderr = self.shell.run(f"brew install {packages_str}")
        return code == 0

def get_package_manager() -> PackageManager:
    system = platform.system().lower()
    if system == "linux":
        return AptManager()
    elif system == "darwin":
        return BrewManager()
    raise NotImplementedError(f"Unsupported platform: {system}")
