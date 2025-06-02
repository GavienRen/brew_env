import os
import shutil
from pathlib import Path
from ..utils.logger import log_info, log_success
from .base import BaseInstaller
import yaml

class PipInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        self.config = self._load_config()
        self.pip_dir = os.path.expanduser("~/.pip")
        self.pip_conf = os.path.join(self.pip_dir, "pip.conf")

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config/config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def check(self) -> bool:
        return False  # 始终覆盖pip配置

    def install(self):
        log_info("配置pip...")
        os.makedirs(self.pip_dir, mode=0o700, exist_ok=True)
        
        # 直接复制配置文件
        pip_conf_template = Path(__file__).parent.parent.parent / "config/pip.conf"
        shutil.copy2(pip_conf_template, self.pip_conf)
        os.chmod(self.pip_conf, 0o600)
        
        log_success(f"pip已配置使用镜像源: {self.config['mirrors']['pip']}")
