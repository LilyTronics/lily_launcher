"""
Launch a command
"""

import os
import shlex
import subprocess


def launch(command):
    command = command.strip()

    # URL
    if command.startswith(('http://', 'https://')):
        os.startfile(command)
        return

    # Existing file/folder
    if os.path.exists(command):
        os.startfile(command)
        return

    # Everything else is treated as a command
    subprocess.Popen(shlex.split(command), shell=False)


def list_files(command):
    items = []
    folder = os.path.abspath(command.split(':')[-1])
    for current_folder, sub_folders, filenames in os.walk(folder):
        sub_folders.sort()
        for filename in filenames:
            rel_path = current_folder[len(folder):].strip(os.sep)
            parts = rel_path.split(os.sep)
            if parts[0] != '':
                parts.append('')
            sub_items = items
            for part in parts:
                if part != '':
                    matches = [i for i in sub_items if i['name'] == part]
                    if len(matches) == 0:
                        index = next(
                            (i for i, item in enumerate(sub_items) if 'command' in item),
                            len(sub_items)
                        )
                        sub_items.insert(
                            index,
                            {
                                "name": part,
                                "icon": 'folder.png',
                                "items": []
                            }
                        )
                        matches.append(sub_items[index])
                    sub_items = matches[0]['items']
                else:
                    icon_name = 'file'
                    ext = os.path.splitext(filename)[1].strip('.')
                    if ext != '':
                        icon_name += '_' + ext
                    sub_items.append(
                        {
                            "name": filename,
                            "icon": f'{icon_name}.png',
                            "command": os.path.join(current_folder, filename)
                        }
                    )
    return items


if __name__ == '__main__':

    _items = list_files('list_files:src')
    for _item in _items:
        print(_item)
