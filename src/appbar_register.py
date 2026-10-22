"""
Register the app as a side bar.
"""

import ctypes

from ctypes import wintypes

from PySide6.QtWidgets import QApplication


# --------------------------------------------------
# Windows AppBar definitions
# --------------------------------------------------

ABM_NEW = 0x00000000
ABM_REMOVE = 0x00000001
ABM_QUERYPOS = 0x00000002
ABM_SETPOS = 0x00000003

LEFT_RIGTH = { 'default': 0, 'left': 0, 'right': 2 }

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]

# pylint: disable=invalid-name
# pylint: disable=attribute-defined-outside-init
class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", RECT),
        ("lParam", wintypes.LPARAM),
    ]


shell32 = ctypes.windll.shell32
user32 = ctypes.windll.user32


def register_appbar(view, side='left'):
    qt_screen = QApplication.primaryScreen().geometry()
    win_width = user32.GetSystemMetrics(0)
    win_height = user32.GetSystemMetrics(1)
    scale_x = qt_screen.width() / win_width
    scale_y = qt_screen.height() / win_height

    side = LEFT_RIGTH.get(side, LEFT_RIGTH['default'])
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    bar_width = int(view.sizeHint().width() / scale_x)
    hwnd = int(view.winId())

    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd

    shell32.SHAppBarMessage(ABM_NEW, ctypes.byref(abd))

    abd.uEdge = side
    abd.rc.top = 0
    abd.rc.bottom = screen_height
    if side == 2:
        # Right side
        abd.rc.left = screen_width - bar_width
        abd.rc.right = screen_width
    else:
        # Left side
        abd.rc.left = 0
        abd.rc.right = bar_width

    shell32.SHAppBarMessage(ABM_QUERYPOS, ctypes.byref(abd))
    shell32.SHAppBarMessage(ABM_SETPOS, ctypes.byref(abd))

    view.setGeometry(
        int(abd.rc.left * scale_x),
        int(abd.rc.top * scale_y),
        int((abd.rc.right - abd.rc.left) * scale_x),
        int((abd.rc.bottom - abd.rc.top) * scale_y),
    )

def unregister_appbar(view):
    hwnd = int(view.winId())
    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd
    shell32.SHAppBarMessage(ABM_REMOVE, ctypes.byref(abd))


if __name__ == "__main__":

    from src.main import main

    main()
