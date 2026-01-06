from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class PlaceholderView(QWidget):
    def __init__(self, text, on_back):
        super().__init__()

        root = QVBoxLayout()
        root.setAlignment(Qt.AlignTop)
        root.setSpacing(16)

        # Geri dön
        back_btn = QPushButton("← Geri Dön")
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(on_back)
        root.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Metin
        label = QLabel(text)
        label.setStyleSheet("font-size:16px; color:gray;")
        root.addWidget(label)

        self.setLayout(root)