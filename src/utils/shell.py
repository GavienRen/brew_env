import subprocess
import getpass
from typing import Tuple, Optional

class Shell:
    _sudo_password = None  # 类变量保存sudo密码
    
    @staticmethod
    def run(command: str, check: bool = True, need_sudo: bool = False) -> Tuple[int, str, str]:
        """
        执行shell命令
        :param command: 要执行的命令
        :param check: 是否检查返回值
        :param need_sudo: 是否需要sudo权限
        :return: (返回码, 标准输出, 标准错误)
        """
        try:
            if need_sudo:
                if Shell._sudo_password is None:
                    Shell._sudo_password = getpass.getpass("[sudo] password: ")
                
                # 使用已保存的密码执行sudo命令
                auth_cmd = f"echo '{Shell._sudo_password}' | sudo -S -v"
                auth_process = subprocess.run(
                    auth_cmd,
                    shell=True,
                    text=True,
                    capture_output=True
                )
                if auth_process.returncode != 0:
                    Shell._sudo_password = None  # 清除无效密码
                    return 1, "", f"sudo认证失败: {auth_process.stderr}"
                
                command = f"echo '{Shell._sudo_password}' | sudo -S {command}"

            process = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True
            )
            
            if check and process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, command, process.stdout, process.stderr
                )
            return process.returncode, process.stdout, process.stderr
            
        except subprocess.CalledProcessError as e:
            return e.returncode, e.stdout, e.stderr
        except Exception as e:
            return 1, "", str(e)

    @staticmethod
    def run_sudo(command: str, check: bool = True) -> Tuple[int, str, str]:
        """使用sudo执行命令"""
        return Shell.run(command, check, need_sudo=True)
