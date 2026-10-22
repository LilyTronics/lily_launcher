"""
Launch a command
"""

import os
import shlex
import subprocess


def launch(command):
    command = command.strip()

    # URL
    if command.startswith(("http://", "https://")):
        os.startfile(command)
        return

    # Existing file/folder
    if os.path.exists(command):
        os.startfile(command)
        return

    # Everything else is treated as a command
    subprocess.Popen(shlex.split(command), shell=False)
