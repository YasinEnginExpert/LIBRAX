from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)
from PySide6.QtCore import Qt


def loading_screen(text: str):
    container = QWidget()

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    layout.setSpacing(12)

    title = QLabel("LIBRAX")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("""
        QLabel {
            font-size: 26px;
            font-weight: 700;
            letter-spacing: 1px;
        }
    """)

    subtitle = QLabel(text)
    subtitle.setAlignment(Qt.AlignCenter)
    subtitle.setStyleSheet("""
        QLabel {
            color: #6b7280;
            font-size: 14px;
        }
    """)

    hint = QLabel("Lütfen bekleyiniz...")
    hint.setAlignment(Qt.AlignCenter)
    hint.setStyleSheet("color: #9ca3af; font-size: 12px;")

    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addWidget(hint)

    container.setLayout(layout)
    return container
