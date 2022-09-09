from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QComboBox, QLabel, QRadioButton, QPushButton, QWidget


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(480, 480)

        # Setup UI
        self.combo_box = QComboBox(self)
        self.udp_btn = QRadioButton('UDP', self)

        self.setup_ui()

    def setup_labels(self):
        labels = (
            (
                'Surfshark Config Generator',  # Text
                (0, 20, 480, 60),  # Geometry (left, top, width, height)
                24  # Size
            ),
            (
                'Locations:',
                (0, 150, 480, 40),
                18
            )
        )

        for (text, geo, size) in labels:
            lbl = QLabel(text, self)
            lbl.setGeometry(QRect(*geo))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f'font-size: {size}px; font-weight: bold')

    def setup_radio_buttons(self):
        style = 'font-size: 14px; font-weight: bold'

        self.udp_btn.setGeometry(QRect(180, 240, 60, 30))
        self.udp_btn.setStyleSheet(style)
        self.udp_btn.setChecked(True)

        radio_btn = QRadioButton('TCP', self)
        radio_btn.setStyleSheet(style)
        radio_btn.setGeometry(QRect(250, 240, 60, 30))

    def setup_ui(self):
        self.setup_labels()
        self.setup_radio_buttons()

        # ComboBox
        self.combo_box.setGeometry(QRect(30, 200, 420, 30))
        self.combo_box.setStyleSheet('font-size: 16px;')

        button = QPushButton('Generate', self)
        button.setGeometry(QRect(30, 420, 420, 40))
        button.clicked.connect(self.on_click)

        self.setWindowTitle('Surfshark Config Generate')
        self.setWindowIcon(QIcon('app.ico'))

    # Generate Button Clicked
    def on_click(self):
        raise NotImplementedError
