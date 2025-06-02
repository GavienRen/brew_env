import os
import yaml
from pathlib import Path
from ..utils.logger import log_info, log_success, log_error, log_warning
from .base import BaseInstaller

class SSHInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        self.config = self._load_config()["git"]  # 仍使用git配置中的email

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config/config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def check(self) -> bool:
        """检查SSH密钥是否存在且配置正确"""
        ssh_pub_key = os.path.expanduser("~/.ssh/id_rsa.pub")
        if not os.path.exists(ssh_pub_key):
            return False
            
        # 检查密钥邮箱
        code, current_email, _ = self.shell.run(f"grep -o '[^ ]*@[^ ]*$' {ssh_pub_key}")
        if code == 0 and current_email.strip() == self.config['user']['email']:
            # 显示现有密钥信息
            with open(ssh_pub_key) as f:
                pub_key = f.read().strip()
            log_info(f"已配置SSH密钥 ({current_email.strip()})")
            return True
        return False

    def install(self):
        log_info("配置SSH...")
        ssh_dir = os.path.expanduser("~/.ssh")
        ssh_key = os.path.join(ssh_dir, "id_rsa")
        
        # 确保.ssh目录存在
        os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
        
        # 检查是否已存在密钥
        if os.path.exists(ssh_key):
            log_info("检测到已存在的SSH密钥，先备份...")
            self.shell.run(f"mv {ssh_key} {ssh_key}.bak")
            self.shell.run(f"mv {ssh_key}.pub {ssh_key}.pub.bak")
        
        # 使用-N ''设置空密码,-f指定输出文件,-C设置注释
        log_info("生成新的SSH密钥...")
        cmd = f'ssh-keygen -t rsa -N "" -f "{ssh_key}" -C "{self.config["user"]["email"]}"'
        
        code, stdout, stderr = self.shell.run(cmd)
        if code == 0:
            # 设置正确的权限
            os.chmod(ssh_key, 0o600)
            os.chmod(f"{ssh_key}.pub", 0o644)
            log_success("SSH密钥生成完成")
            
            # 显示公钥内容方便复制
            with open(f"{ssh_key}.pub") as f:
                pub_key = f.read().strip()
            log_info(f"SSH公钥:\n{pub_key}")
        else:
            log_error(f"SSH密钥生成失败: {stderr}")
            # 如果失败，恢复备份
            if os.path.exists(f"{ssh_key}.bak"):
                self.shell.run(f"mv {ssh_key}.bak {ssh_key}")
                self.shell.run(f"mv {ssh_key}.pub.bak {ssh_key}.pub")
                log_warning("已恢复原有SSH密钥")
