"""
Reads the config file.
Monitors for changes.
"""

import json
import threading
import time

from src.run_command import list_files


class ConfigReader():

    _MONITOR_INTERVAL = 1

    def __init__(self, filename):
        self._filename = filename
        self._settings = None
        self._launchers = None
        self._callback = None
        threading.Thread(target=self._check_for_changes, daemon=True).start()

    ###########
    # Private #
    ###########

    def _create_style_sheet(self):
        style_sheet = ''
        # Frame background
        value = self._settings.get('frame_background')
        if value is not None:
            style_sheet += f'QWidget {{ background-color: {value}; }} '
        # Label
        style_sheet += 'QLabel { font-size: 8px; padding: 0; margin: 0; '
        value = self._settings.get('text_color')
        if value is not None:
            style_sheet += f'color: {value}; '
        style_sheet += '} '
        # Button style
        style_sheet += 'QPushButton { padding: 4px; border: none; '
        value = self._settings.get('button_background')
        if value is not None:
            style_sheet += f'background-color: {value}; '
        style_sheet += '} '
        value = self._settings.get('button_hover_background')
        if value is not None:
            style_sheet += f'QPushButton:hover {{ background-color: {value}; }} '
        # Menu
        style_sheet += 'QMenu { padding: 8px; font-size: 16px; menu-scrollable: 1;'
        value = self._settings.get('menu_text_color')
        if value is not None:
            style_sheet += f'color: {value}; '
        value = self._settings.get('frame_background')
        if value is not None:
            style_sheet += f'background-color: {value}; '
        style_sheet += '} '
        style_sheet += 'QMenu::item { padding: 4px 24px 4px 4px; margin: 2px;} '
        style_sheet += 'QMenu::item:selected { '
        value = self._settings.get('menu_hover_color')
        if value is not None:
            style_sheet += f'color: {value}; '
        value = self._settings.get('menu_hover_background')
        if value is not None:
            style_sheet += f'background-color: {value}; '
        style_sheet += '} '
        return style_sheet

    def _update_launchers(self, launchers):
        for launcher in launchers:
            if 'items' in launcher:
                self._update_launchers(launcher['items'])
            elif 'command' in launcher:
                if launcher['command'].startswith('list_files:'):
                    items = list_files(launcher['command'])
                    launcher.pop('command')
                    launcher['items'] = items
        return launchers

    def _check_for_changes(self):
        while True:
            try:
                data = json.load(open(self._filename, 'r', encoding='utf-8'))
                settings = data.get('settings', {})
                launchers = self._update_launchers(data.get('launchers', []))
                if launchers != self._launchers or settings != self._settings:
                    self._settings = settings
                    self._launchers = launchers
                    if callable(self._callback):
                        self._callback(self._launchers, self._create_style_sheet())
            except Exception:
                pass
            time.sleep(self._MONITOR_INTERVAL)

    ##########
    # Public #
    ##########

    def set_callback(self, callback):
        self._callback = callback


if __name__ == '__main__':

    from src.runtime import Runtime


    def _test_callback(config, style_sheet):
        print('Config changed:')
        print(config)
        print(style_sheet)


    reader = ConfigReader(Runtime.config_filename())
    reader.set_callback(_test_callback)

    input('Press enter to stop\n')
