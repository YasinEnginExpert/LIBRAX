from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt

from internal.app.state import Session


class LoginView(QWidget):
    def __init__(self, state, auth_repo, on_success):
        super().__init__()

        self.state = state
        self.auth_repo = auth_repo
        self.on_success = on_success

        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("LIBRAX")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
            }
        """)

        subtitle = QLabel("Kütüphane Yönetim Sistemi")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Kullanıcı adı")
        self.user_input.setClearButtonEnabled(True)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Şifre")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Giriş")
        self.login_btn.setDefault(True)
        self.login_btn.clicked.connect(self.login)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.user_input)
        main_layout.addWidget(self.pass_input)
        main_layout.addWidget(self.login_btn)

        self.setLayout(main_layout)

    def login(self):
        username = self.user_input.text().strip()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Eksik Bilgi",
                "Lütfen kullanıcı adı ve şifreyi giriniz."
            )
            return

        self.login_btn.setEnabled(False)

        row = self.auth_repo.login(username, password)

        if row:
            self.state.session = Session(row[0], row[1], row[2])
            self.on_success()
        else:
            QMessageBox.critical(
                self,
                "Giriş Başarısız",
                "Kullanıcı adı veya şifre hatalı."
            )
            self.login_btn.setEnabled(True)
