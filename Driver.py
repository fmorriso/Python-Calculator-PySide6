import sys
from importlib.metadata import version

from PySide6.QtWidgets import (QApplication)

from calculator import Calculator
from gui_settings import GuiSettings


def get_python_version() -> str:
    return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'


def get_package_version(package_name: str) -> str:
    return version(package_name)


if __name__ == "__main__":
    print(f'Python version: {get_python_version()}')
    print(f'PySide6 version: {get_package_version("pyside6")}')
    print(f'PySide6-Addons version: {get_package_version("pyside6-addons")}')
    print(f'PyAutoGUI version: {get_package_version("pyautogui")}')

    gui_settings = GuiSettings(0.65)
    print(f'GUI settings: {gui_settings}')
    app = QApplication(sys.argv)

    window = Calculator(gui_settings.scaled_width, gui_settings.scaled_width)
    window.show()
    app.exec()
