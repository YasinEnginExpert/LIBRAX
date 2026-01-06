from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QGridLayout
)
from PySide6.QtCore import Qt


class DashboardView(QWidget):
    def __init__(self, state, on_nav, on_logout):
        super().__init__()
        self.state = state
        self.on_nav = on_nav
        self.on_logout = on_logout

        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout()
        root.setAlignment(Qt.AlignTop)
        root.setSpacing(16)

        # ===== Kullanıcı adı =====
        username = "?"
        if self.state.session:
            username = self.state.session.kullanici_adi
        title = QLabel(f"Hoş geldiniz, {username}")
        title.setStyleSheet(
            "font-size:20px; font-weight:600;"
        )
        root.addWidget(title)

        subtitle = QLabel("Lütfen bir işlem seçin:")
        subtitle.setStyleSheet("color:gray;")
        root.addWidget(subtitle)

        # ===== Menü =====
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        buttons = [
            ("Üye Yönetimi", "members"),
            ("Kitap Yönetimi", "books"),
            ("Ödünç Ver", "borrow"),
            ("Teslim Al", "return"),
            ("Ceza Görüntüleme", "penalties"),
            ("Raporlar", "reports"),
            ("Dinamik Sorgu", "dynamic_query"),
        ]

        for i, (text, key) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setMinimumHeight(42)
            btn.clicked.connect(
                lambda _, k=key: self.on_nav(k)
            )
            grid.addWidget(btn, i // 2, i % 2)

        root.addLayout(grid)

        # ===== Çıkış =====
        logout_btn = QPushButton("Çıkış")
        logout_btn.setMinimumHeight(42)
        logout_btn.setStyleSheet("font-weight:600;")
        logout_btn.clicked.connect(self.on_logout)
        root.addWidget(logout_btn)

        self.setLayout(root)
