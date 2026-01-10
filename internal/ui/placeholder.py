from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QLabel, QPushButton
)
from PySide6.QtCore import Qt


class PlaceholderView(QWidget):
    def __init__(self, text: str, on_back):
        super().__init__()
        self.text = text
        self.on_back = on_back

        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout()
        root.setAlignment(Qt.AlignTop)
        root.setSpacing(16)

        # ===== GERİ =====
        back_btn = QPushButton("← Geri Dön")
        back_btn.setFixedWidth(120)
        back_btn.setStyleSheet("font-weight:600;")
        back_btn.clicked.connect(self.on_back)
        root.addWidget(back_btn, alignment=Qt.AlignLeft)

        # ===== BAŞLIK =====
        title = QLabel("Sayfa Hazırlanıyor")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
            }
        """)
        root.addWidget(title)

        # ===== AÇIKLAMA =====
        label = QLabel(self.text)
        label.setWordWrap(True)
        label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #6b7280;
            }
        """)
        root.addWidget(label)

        self.setLayout(root)
