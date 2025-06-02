import os
from pathlib import Path
import yaml
from ..utils.logger import log_info
from .base import BaseInstaller

class ZshInstaller(BaseInstaller):
    def __init__(self):
        super().__init__()
        self.config = self._load_config()["zsh"]
        self.oh_my_zsh_dir = os.path.expanduser("~/.oh-my-zsh")

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config/config.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def check(self) -> bool:
        return os.path.exists(self.oh_my_zsh_dir)

    def install(self):
        log_info("安装Oh My Zsh...")
        
        # 安装Oh My Zsh
        install_cmd = 'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'
        self.shell.run(install_cmd)
        
        # 配置主题
        self._configure_theme()
        
        # 安装插件
        self._install_plugins()
        
        # 设置为默认shell
        self.shell.run("chsh -s $(which zsh)")

    def _configure_theme(self):
        theme = self.config["theme"]
        zshrc_path = os.path.expanduser("~/.zshrc")
        log_info(f"配置主题: {theme}")
        # 替换主题配置
        sed_cmd = f"sed -i 's/ZSH_THEME=.*/ZSH_THEME=\"{theme}\"/g' {zshrc_path}"
        self.shell.run(sed_cmd)

    def _install_plugins(self):
        plugins = self.config["plugins"]
        log_info("安装Oh My Zsh插件...")
        for plugin in plugins:
            self._install_plugin(plugin)

    def _install_plugin(self, plugin: str):
        custom_plugins_dir = f"{self.oh_my_zsh_dir}/custom/plugins"
        plugin_dir = f"{custom_plugins_dir}/{plugin}"
        
        if not os.path.exists(plugin_dir):
            log_info(f"安装插件: {plugin}")
            clone_cmd = f"git clone https://github.com/zsh-users/{plugin}.git {plugin_dir}"
            self.shell.run(clone_cmd)
