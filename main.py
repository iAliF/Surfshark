import json
import os.path
import sys
from typing import List

from PySide6.QtWidgets import QApplication, QMessageBox
from qt_material import apply_stylesheet

from ui import MainWidget


class Main(MainWidget):
    CONFIGS_DIR = 'configs'
    LOCATIONS_PATH = 'locations.json'
    DEFAULT_CONFIG_PATH = 'default.ovpn'

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

    def generate_config(self, host: str):
        pass

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
