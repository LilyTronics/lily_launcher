"""
Run time functions
"""

import sys

from pathlib import Path


class Runtime:

    @staticmethod
    def app_dir():
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent
        return Path(__file__).parent.parent

    @classmethod
    def config_filename(cls):
        app_dir = cls.app_dir()
        search_paths = [
            app_dir / 'lily_launcher.json',
            app_dir / 'lib' / 'lily_launcher.json',
            app_dir / 'src' / 'lily_launcher.json'
        ]
        for path in search_paths:
            if path.is_file():
                return str(path)
        return ''

    @classmethod
    def get_icon_path(cls, filename, is_exclamation=False):
        filename = Path(filename)
        if filename.is_file():
            return str(filename)
        # User icons in sub folder of app
        search_paths = [
            cls.app_dir() / 'icons' / filename,
            cls.app_dir() / 'lib' / 'icons' / filename
        ]
        for path in search_paths:
            if path.is_file():
                return str(path)
        # No icon -> exclamation
        if not is_exclamation:
            return cls.get_icon_path('exclamation.png', True)
        return ''


if __name__ == '__main__':

    print(Runtime.app_dir())
    print(Runtime.config_filename())
    print(Runtime.get_icon_path('folder.png'))
