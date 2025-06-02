from pathlib import Path
import yaml
import os
from ..utils.logger import log_info, log_success
from .base import BaseInstaller

class GitInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        self.config = self._load_config()["git"]

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config/config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def check(self) -> bool:
        """检查git是否已安装以及配置是否正确"""
        # 检查git是否安装
        returncode, _, _ = self.shell.run("git --version", check=False)
        if returncode != 0:
            return False
            
        # 检查配置是否一致
        for key, expected in {
            "user.name": self.config["user"]["name"],
            "user.email": self.config["user"]["email"],
            "core.editor": self.config["editor"]
        }.items():
            code, stdout, _ = self.shell.run(f"git config --global {key}")
            if code != 0 or stdout.strip() != expected:
                return False
        return True

    def install(self):
        log_info("配置Git...")
        configs = {
            "user.name": self.config["user"]["name"],
            "user.email": self.config["user"]["email"],
            "core.editor": self.config["editor"]
        }
        
        # 检查并更新每个配置
        for key, value in configs.items():
            code, current, _ = self.shell.run(f"git config --global {key}")
            if code != 0 or current.strip() != value:
                self.shell.run(f"git config --global {key} '{value}'")
                log_success(f"Git {key} 已更新为 {value}")
            else:
                log_info(f"Git {key} 已配置为 {value}")

class SSHInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        self.config = self._load_config()["ssh"]

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config/setup.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def check(self) -> bool:
        """检查SSH密钥是否已配置"""
        ssh_pub_key = os.path.expanduser("~/.ssh/id_rsa.pub")
        if os.path.exists(ssh_pub_key):
            code, current_email, _ = self.shell.run(f"grep -o '[^ ]*@[^ ]*$' {ssh_pub_key}")
            if code == 0 and current_email.strip() == self.config['user']['email']:
                return True
        return False

    def install(self):
        log_info("配置SSH密钥...")
        ssh_pub_key = os.path.expanduser("~/.ssh/id_rsa.pub")
        if os.path.exists(ssh_pub_key):
            log_info("检查SSH密钥...")
            code, current_email, _ = self.shell.run(f"grep -o '[^ ]*@[^ ]*$' {ssh_pub_key}")
            if code == 0 and current_email.strip() == self.config['user']['email']:
                log_info("SSH密钥已配置且邮箱正确")
                return

        log_info("生成SSH密钥...")
        self.shell.run(f"ssh-keygen -t rsa -C '{self.config['user']['email']}'")
        log_success("SSH密钥生成完成")
