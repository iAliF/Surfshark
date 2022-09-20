import json
import os.path
import sys
from typing import List, Optional

import requests
from PySide6.QtWidgets import QApplication, QMessageBox
from qt_material import apply_stylesheet
from requests import RequestException

from ui import MainWidget


class Main(MainWidget):
    CONFIGS_DIR = 'configs'
    LOCATIONS_PATH = 'resources/locations.json'
    DEFAULT_CONFIG_PATH = 'resources/default.ovpn'

    def __init__(self, parent=None):
        super().__init__(parent)

        self.locations: List[List[str, str]] = []
        self.default_config = None

        self.create_configs_dir()
        self.load_locations()
        self.load_config()

    def create_configs_dir(self) -> None:
        if not os.path.exists(self.CONFIGS_DIR):
            os.mkdir(self.CONFIGS_DIR)

    def load_locations(self) -> None:
        self.check_file_exists(self.LOCATIONS_PATH)

        with open(self.LOCATIONS_PATH) as file:
            self.locations = json.load(file)

        # Add locations to ComboBox
        self.combo_box.addItems(
            (x[0] for x in self.locations)
        )

    def load_config(self):
        self.check_file_exists(self.DEFAULT_CONFIG_PATH)

        with open(self.DEFAULT_CONFIG_PATH) as file:
            self.default_config = file.read()

    def on_click(self):
        current = self.locations[self.combo_box.currentIndex()][1]
        self.generate_config(current)

    def generate_config(self, host: str) -> None:
        ip = self.get_ip(host)
        if ip is None:
            return

        config = self.default_config
        config = config.replace('<<<REMOTE>>>', ip).replace('<<<TYPE>>>', 'udp' if self.udp_btn.isChecked() else 'tcp')

        file_name = os.path.join(
            self.CONFIGS_DIR,
            f'{self.combo_box.currentText()}.ovpn'
        )

        with open(file_name, 'w') as file:
            file.write(config)

        self.show_message_box(
            QMessageBox.NoIcon,
            'Done',
            'Config Successfully generated and saved into configs directory',
            False
        )

    def get_ip(self, host) -> Optional[str]:
        try:
            req = requests.get(f'http://ip-api.com/line/{host}?fields=query', timeout=5)
            return req.text.strip()
        except RequestException:
            self.show_message_box(
                QMessageBox.Critical,
                'Error',
                'Cannot send request',
                False
            )
            return None

    def check_file_exists(self, file: str) -> None:
        if not (os.path.exists(file) and os.path.isfile(file)):
            self.show_message_box(
                QMessageBox.Critical,
                'File not found',
                f'File {file} not found'
            )

    @staticmethod
    def show_message_box(icon: QMessageBox.Icon, title: str, text: str, exit_app: bool = True) -> None:
        box = QMessageBox(
            icon,
            title,
            text,
            QMessageBox.Ok
        )

        box.exec()

        if exit_app:
            exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, 'light_purple.xml')

    main = Main()
    main.show()
    sys.exit(app.exec())
