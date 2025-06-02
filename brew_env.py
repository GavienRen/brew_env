#!/usr/bin/env python3
import platform
import argparse
from src.installers.system import SystemInstaller
from src.installers.git import GitInstaller
from src.installers.zsh import ZshInstaller
from src.installers.ssh import SSHInstaller
from src.utils.logger import log_info, log_success, log_error
from src.installers.pip import PipInstaller


def main():
    parser = argparse.ArgumentParser(description='系统配置工具')
    parser.add_argument('--change-source', action='store_true',
                        help='更换软件源(默认不更换)')
    args = parser.parse_args()

    platform_name = "macOS" if platform.system().lower() == "darwin" else "Ubuntu"
    log_info(f"🚀 开始 {platform_name} 系统配置...")

    installers = [
        SystemInstaller(change_source=args.change_source),  # 🔧 系统设置
        GitInstaller(),      # 📦 Git配置
        SSHInstaller(),      # 🔑 SSH配置
        PipInstaller(),      # 🐍 Python包管理
        ZshInstaller(),      # 🐚 Shell配置
    ]

    for installer in installers:
        try:
            installer.run()
        except Exception as e:
            log_error(f"❌ 安装失败: {str(e)}")
            raise

    log_success("✨ 系统配置完成！")


if __name__ == "__main__":
    main()
