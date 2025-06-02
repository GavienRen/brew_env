from abc import ABC, abstractmethod
import platform
from ..utils.logger import log_info, log_success, log_error, log_warning
from ..utils.shell import Shell
from pathlib import Path
import yaml

class BaseInstaller(ABC):
    def __init__(self):
        self.shell = Shell()
        self.platform = platform.system().lower()
    
    @abstractmethod
    def install(self):
        """安装方法必须被子类实现"""
        pass
    
    @abstractmethod
    def check(self) -> bool:
        """检查是否已安装"""
        pass

    def run(self):
        """运行安装流程"""
        if not self.is_platform_supported():
            log_warning(f"{self.__class__.__name__} 不支持当前平台")
            return
            
        if self.check():
            log_warning(f"{self.__class__.__name__} 已经安装")
            return
        self.install()
        
    def is_platform_supported(self) -> bool:
        """检查当前平台是否支持"""
        return True

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config/config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)
