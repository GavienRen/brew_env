import yaml
import os
from pathlib import Path
from ..utils.package_manager import get_package_manager
from ..utils.logger import log_info, log_error, log_success, log_warning
from .base import BaseInstaller

class SystemInstaller(BaseInstaller):
    def __init__(self, change_source: bool = False):
        super().__init__()
        self.change_source = change_source
        self.config = self._load_config()
        self.package_manager = get_package_manager()

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config/config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def check(self) -> bool:
        # 系统配置总是需要执行
        return False

    def install(self):
        if self.change_source:
            self._update_sources()
            if not self.package_manager.update():
                log_error("更新软件包列表失败，继续安装...")
        else:
            log_info("跳过更新软件源和软件包列表 💤")

        self._install_packages()
        self._setup_repo()
        self._setup_pip()
        self._setup_github_hosts()

    def _update_sources(self):
        if self.platform == "linux":
            mirror = self.config["mirrors"]["linux"]["apt"]
            log_info(f"更新APT源为: {mirror}")
            # 实现APT源更新逻辑
        elif self.platform == "darwin":
            mirror = self.config["mirrors"]["macos"]["brew"]
            log_info(f"更新Homebrew源为: {mirror}")
            # 实现Homebrew源更新逻辑

    def _install_packages(self):
        # 收集所有需要安装的包
        all_packages = self.config["packages"]["common"]
        platform_key = "linux" if self.platform == "linux" else "macos"
        if platform_key in self.config["packages"]:
            all_packages.extend(self.config["packages"][platform_key])

        # 批量安装
        log_info("🚀 开始批量安装软件包...")
        if not self.package_manager.batch_install(all_packages):
            log_error("部分包安装失败")
            return
        log_success("✨ 所有软件包安装完成")

    def _install_package(self, package: str):
        try:
            log_info(f"安装 {package}...")
            if not self.package_manager.install(package):
                log_error(f"安装 {package} 失败，继续安装其他包...")
            else:
                log_success(f"{package} 安装成功")
        except KeyboardInterrupt:
            log_warning(f"用户中断安装 {package}")
            raise
        except Exception as e:
            log_error(f"安装 {package} 时发生错误: {str(e)}")

    def _setup_repo(self):
        """配置repo工具"""
        log_info("配置repo工具...")
        repo_url = "https://mirrors.tuna.tsinghua.edu.cn/git/git-repo"
        code, _, _ = self.shell.run_sudo(f"curl {repo_url} -o /usr/bin/repo")
        if code == 0:
            self.shell.run_sudo("chmod +x /usr/bin/repo")
            log_success("repo工具配置完成")
        else:
            log_error("repo工具配置失败")

    def _setup_pip(self):
        """配置pip"""
        pip_dir = os.path.expanduser("~/.pip")
        if not os.path.exists(pip_dir):
            log_info("配置pip...")
            os.makedirs(pip_dir, exist_ok=True)
            pip_conf = Path(__file__).parent.parent.parent / "pip.conf"
            os.system(f"cp {pip_conf} {pip_dir}/pip.conf")
            log_success("pip配置完成")

    def _setup_github_hosts(self):
        """配置GitHub加速"""
        log_info("配置GitHub Hosts加速...")

       # https://gitee.com/klmahuaw/GitHub520
       # sudo sh -c 'sed -i "/# GitHub520 Host Start/Q" /etc/hosts && curl https://raw.hellogithub.com/hosts >> /etc/hosts'
 
        # 先下载最新hosts
        tmp_hosts = "/tmp/github_hosts"
        download_cmd = f"curl -s https://raw.hellogithub.com/hosts -o {tmp_hosts}"
        if self.shell.run(download_cmd)[0] != 0:
            log_error("下载GitHub hosts失败")
            return
            
        # 清理旧的配置
        clean_cmd = f'sudo sed -i "/# GitHub520 Host Start/,/# GitHub520 Host End/d" /etc/hosts'
        if self.shell.run_sudo(clean_cmd)[0] != 0:
            log_error("清理旧GitHub hosts失败")
            return
            
        # 添加新配置
        append_cmd = f"sudo bash -c 'cat {tmp_hosts} >> /etc/hosts'"
        if self.shell.run(append_cmd)[0] != 0:
            log_error("添加新GitHub hosts失败")
            return
            
        # 清理临时文件
        os.remove(tmp_hosts)
        log_success("GitHub Hosts配置完成")
