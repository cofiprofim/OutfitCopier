from rgbprint import Color, rgbprint
from datetime import datetime
import os
import re
import shutil

from __main__ import VERSION
from typing import (
    Optional,
    NoReturn,
    Callable
)

__all__ = ("Display", "Tools")


GRAY_COLOR = Color(168, 168, 168)

MAIN_COLOR = Color(205, 0, 236)
ACCENT_COLOR = Color(112, 102, 114)

SIGNATURE = f"Outfit Changing Tool v{VERSION}"
TITLE = r"""  ____        _    __ _ _    _____            _             
 / __ \      | |  / _(_) |  / ____|          (_)           
| |  | |_   _| |_| |_ _| |_| |     ___  _ __  _  ___ _ __  
| |  | | | | | __|  _| | __| |    / _ \| '_ \| |/ _ \ '__| 
| |__| | |_| | |_| | | | |_| |___| (_) | |_) | |  __/ |    
 \____/ \__,_|\__|_| |_|\__|\_____\___/| .__/|_|\___|_|    
                                       | |                 
                                       |_|                 

"""


def _print_centered(text: str, color: Optional[Color] = None, end: str = "\n") -> None:

    def _get_terminal_size() -> int:
        return shutil.get_terminal_size().columns

    def _remove_color_codes(text: str) -> str:
        return re.sub(r"\033\[[0-9;]*m", "", text)

    terminal_size = _get_terminal_size()

    for line in text.splitlines():
        indent = (terminal_size - len(_remove_color_codes(line))) // 2
        rgbprint((" " * indent) + line, color=color, end=end)


def _timestamp_wrap(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        func(*args, _timestamp=timestamp, **kwargs)
    
    return wrapper


class Tools:
    def exit_program(error_code: Optional[int] = None) -> NoReturn:
        os.system("pause" if os.name == "nt" else "read -p \"Press any key to continue . . .\"")
        os._exit(error_code or 0)


    def clear_console() -> None:
        os.system("cls" if os.name == "nt" else "clear")


class Display:
    timestamp_color = Color(190, 190, 190)
    info_color = Color(127, 127, 127)
    success_color = Color(0, 255, 0)
    exception_color = Color(255, 0, 0)
    error_color = Color(255, 0, 0)
    input_color = Color(84, 84, 84)
    reset_color = Color.reset
    
    def main() -> None:
        _print_centered(TITLE, MAIN_COLOR)
        _print_centered(SIGNATURE, ACCENT_COLOR, end="\n\n\n")
    
    @classmethod
    @_timestamp_wrap
    def info(cls, text: str, end: str = "\n", *, _timestamp) -> None:
        print(f"{cls.timestamp_color}{_timestamp} > {cls.info_color}INFO{cls.reset_color} | {text}", end=end)


    @classmethod
    @_timestamp_wrap
    def success(cls, text: str, end: str = "\n", *, _timestamp) -> None:
        print(f"{cls.timestamp_color}{_timestamp} > {cls.success_color}SUCCESS{cls.reset_color} | {text}", end=end)


    @classmethod
    @_timestamp_wrap
    def exception(cls, text: str, end: str = "\n", *, _timestamp) -> NoReturn:
        print(f"{cls.timestamp_color}{_timestamp} > {cls.exception_color}FATAL{cls.reset_color} | {text}", end=end)
        Tools.exit_program()
        

    @classmethod
    @_timestamp_wrap
    def error(cls, text: str, end: str = "\n", *, _timestamp) -> None:
        print(f"{cls.timestamp_color}{_timestamp} > {cls.error_color}ERROR{cls.reset_color} | {text}", end=end)


    @classmethod
    async def user_input(cls, text: str) -> str:
        _timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        choice = input(f"{cls.timestamp_color}{_timestamp} > {cls.input_color}INPUT{cls.reset_color} | {text}")
        return choice.strip()
