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

    # ================= UI =================

    def _build_ui(self):
        root = QVBoxLayout()
        root.setSpacing(14)
        root.setAlignment(Qt.AlignCenter)

        title = QLabel("LIBRAX")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: 700;
                letter-spacing: 1px;
            }
        """)

        subtitle = QLabel("Kütüphane Yönetim Sistemi")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6b7280;")

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Kullanıcı adı")
        self.user_input.setClearButtonEnabled(True)
        self.user_input.returnPressed.connect(self.login)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Şifre")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.returnPressed.connect(self.login)

        self.login_btn = QPushButton("Giriş Yap")
        self.login_btn.setDefault(True)
        self.login_btn.setMinimumHeight(36)
        self.login_btn.clicked.connect(self.login)

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addSpacing(12)
        root.addWidget(self.user_input)
        root.addWidget(self.pass_input)
        root.addWidget(self.login_btn)

        self.setLayout(root)

    # ================= LOGIC =================

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

        self._set_loading(True)

        try:
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
                self._set_loading(False)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Giriş sırasında hata oluştu:\n{e}"
            )
            self._set_loading(False)

    def _set_loading(self, loading: bool):
        self.login_btn.setEnabled(not loading)
        text = "Giriş Yapılıyor..." if loading else "Giriş Yap"
        self.login_btn.setText(text)
