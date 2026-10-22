"""
Build the executable
"""

import subprocess
import shutil
import time

from pathlib import Path

VERSION = '1.0.0'


def build_exe():
    print('Clean old builds')
    for folder in ["build", "dist"]:
        if Path(folder).exists():
            shutil.rmtree(folder)
    # Some times the folder is not actually removed before pyinstaller starts
    time.sleep(2)

    print('Prepare version info')
    version_tuple = ", ".join(VERSION.split(".")) + ", 0"
    with open('src/version_info_template.txt', 'r', encoding='utf_8') as fp:
        content = fp.read()
    content = content.replace('_VERSION_TUPLE_', version_tuple)
    content = content.replace('_VERSION_STRING_', VERSION)
    with open('version_info.txt', 'w', encoding='utf-8') as fp:
        fp.write(content)

    print('Run PyInstaller')
    subprocess.run(
        [
            "pyinstaller",
            "--windowed",
            "--add-data", "icons;icons",
            "--add-data", "src/lily_launcher.json;.",
            "--contents-directory", "lib",
            "--name", "LilyLauncher",
            "--version-file", "version_info.txt",
            "src/main.py"
        ],
        check=True,
    )

    print('Remove build output')
    for folder in ["build"]:
        if Path(folder).exists():
            shutil.rmtree(folder)
    Path('version_info.txt').unlink()


if __name__ == '__main__':

    build_exe()
