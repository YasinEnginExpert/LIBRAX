from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


def loading_screen(text: str):
    lbl = QLabel(text)
    lbl.setAlignment(Qt.AlignCenter)
    return lbl
