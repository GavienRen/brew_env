import logging
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


class _Logger:
    def __init__(self):
        self._logger = logging.getLogger('brew_env')
        self._logger.setLevel(logging.INFO)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(message)s'))
            self._logger.addHandler(handler)

    def _format_message(self, message: str) -> str:
        timestamp = datetime.now().strftime('%H:%M:%S')
        return f"[{timestamp}] {message}"

    def info(self, message):
        self._logger.info(f"{Fore.CYAN}{self._format_message(message)}{Style.RESET_ALL}")

    def success(self, message):
        self._logger.info(f"{Fore.GREEN}{self._format_message(message)}{Style.RESET_ALL}")

    def error(self, message):
        self._logger.error(f"{Fore.RED}{self._format_message(message)}{Style.RESET_ALL}")

    def warning(self, message):
        self._logger.warning(f"{Fore.YELLOW}{self._format_message(message)}{Style.RESET_ALL}")


# 全局单例
_logger = _Logger()

# 全局函数


def log_info(message): _logger.info(message)
def log_warning(message): _logger.warning(message)
def log_error(message): _logger.error(message)
def log_success(message): _logger.success(message)
