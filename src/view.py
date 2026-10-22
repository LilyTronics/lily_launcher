"""
Application view.
"""

from PySide6.QtCore import QPoint
from PySide6.QtCore import Qt
from PySide6.QtCore import QSize
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from src.appbar_register import unregister_appbar
from src.run_command import launch
from src.runtime import Runtime


class View(QWidget):

    FRAME_PADDING = 8
    BUTTON_SPACING = 8
    BUTTON_SIZE = 40
    ICON_SIZE = 32
    MENU_EDGE_OVERLAP = 2

    update_gui = Signal(list, str)

    def __init__(self, version):
        super().__init__()
        self._version = version
        self.setWindowTitle('Dock Sidebar')
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.Tool)
        self.update_gui.connect(self._on_update_gui)
        self._setup_ui()
        self.adjustSize()

    ###########
    # Private #
    ###########

    def _setup_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(*(self.FRAME_PADDING,) * 4)
        self._layout.setSpacing(self.BUTTON_SPACING)
        # Add dummy button for Window width, set heigh to 0 so we don't see the button
        # The button will be one after the first GUI update
        button = QPushButton()
        button.setFixedSize(self.BUTTON_SIZE, 0)
        self._layout.addWidget(button)

    def _load_icon(self, filename):
        icon_filename = Runtime.get_icon_path(filename)
        return QIcon(icon_filename)

    def _on_button_click(self, item, button):
        if 'command' in item:
            launch(item['command'])
        if 'items' in item:
            self._show_menu(item, button)

    def _show_menu(self, item, button):
        menu = QMenu(self)
        self._build_menu(menu, item['items'])
        menu.adjustSize()
        menu.setFixedWidth(menu.sizeHint().width() + 20)
        x = self.mapToGlobal(QPoint(self.width(), 0)).x() - self.MENU_EDGE_OVERLAP
        y = button.mapToGlobal(QPoint(0, 0)).y()
        menu.exec(QPoint(x, y))

        # menu.exec(button.mapToGlobal(self.rect().topRight()))

    def _build_menu(self, menu, items):
        for item in items:
            if 'items' in item:
                submenu = QMenu(item['name'], self)
                submenu.setIcon(self._load_icon(item.get('icon')))
                self._build_menu(submenu, item['items'])
                submenu.adjustSize()
                submenu.setFixedWidth(submenu.sizeHint().width())
                menu.addMenu(submenu)
            else:
                action = QAction(self._load_icon(item.get('icon')), item['name'], self)
                action.triggered.connect(
                    lambda checked=False, command=item['command']: launch(command)
                )
                menu.addAction(action)

    def _on_update_gui(self, config, style_sheet):
        self.setStyleSheet(style_sheet)
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        for item in config:
            button = QPushButton()
            button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            button.setToolTip(item['name'])
            button.setIcon(self._load_icon(item.get('icon')))
            button.setIconSize(QSize(self.ICON_SIZE, self.ICON_SIZE))
            button.clicked.connect(
                lambda checked=False, item=item, button=button: self._on_button_click(item, button)
            )
            self._layout.addWidget(button)
        self._layout.addStretch()
        exit_button = QPushButton()
        exit_button.setStyleSheet('QPushButton { border-radius: 20px; }')
        exit_button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        exit_button.setToolTip('Close laucher')
        exit_button.setIcon(self._load_icon('exit.png'))
        exit_button.setIconSize(QSize(self.ICON_SIZE * 0.9, self.ICON_SIZE * 0.9))
        exit_button.clicked.connect(QApplication.instance().quit)
        self._layout.addWidget(exit_button)
        label = QLabel(self._version)
        self._layout.addWidget(label, alignment=Qt.AlignCenter)

    #############
    # Overrides #
    #############

    def enterEvent(self, event):    # pylint: disable=invalid-name
        self.window().activateWindow()
        self.window().raise_()
        super().enterEvent(event)

    def closeEvent(self, event):    # pylint: disable=invalid-name
        unregister_appbar(self)
        super().closeEvent(event)


if __name__ == '__main__':

    from src.main import main

    main()
