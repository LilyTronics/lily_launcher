"""
Main
"""

import sys

from PySide6.QtWidgets import QApplication

from src.appbar_register import register_appbar
from src.config_reader import ConfigReader
from src.view import View

from src.runtime import Runtime
from src.build import VERSION


def main():
    print(f'Runnning from: {Runtime.app_dir()}')

    app = QApplication(sys.argv)
    view = View(VERSION)
    register_appbar(view)
    config_reader = ConfigReader(Runtime.config_filename())
    config_reader.set_callback(view.update_gui.emit)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":

    main()
