from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel,
    QMessageBox
)
from PySide6.QtCore import Qt
from internal.repository.teslim import TeslimRepository


class TeslimView(QWidget):
    def __init__(self, conn, state, on_back):
        super().__init__()
        self.repo = TeslimRepository(conn)
        self.state = state
        self.on_back = on_back
        self.selected_odunc = None

        self._build_ui()
        self.load_data()

    # ===============================
    # UI
    # ===============================
    def _build_ui(self):
        root = QVBoxLayout()
        root.setSpacing(12)

        # ===== GERİ =====
        back_btn = QPushButton("← Geri Dön")
        back_btn.setFixedWidth(120)
        back_btn.setStyleSheet("font-weight:600;")
        back_btn.clicked.connect(self.on_back)
        root.addWidget(back_btn, alignment=Qt.AlignLeft)

        # ===== ARAMA =====
        search_layout = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Üye / Kitap ara")
        self.search.setClearButtonEnabled(True)
        self.search.textChanged.connect(self.load_data)

        search_layout.addWidget(QLabel("Arama:"))
        search_layout.addWidget(self.search)
        root.addLayout(search_layout)

        # ===== TABLO =====
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Üye", "Kitap", "Ödünç Tarihi", "Son Teslim"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellClicked.connect(self.select_row)
        root.addWidget(self.table)

        # ===== TESLİM AL =====
        self.btn = QPushButton("Teslim Al")
        self.btn.setMinimumHeight(40)
        self.btn.setStyleSheet("font-weight:600;")
        self.btn.clicked.connect(self.teslim_al)
        root.addWidget(self.btn)

        self.setLayout(root)

    # ===============================
    # DATA LOAD
    # ===============================
    def load_data(self):
        try:
            rows = self.repo.aktif_oduncler(
                self.search.text().strip()
            )

            self.table.setRowCount(len(rows))
            for i, r in enumerate(rows):
                for c, v in enumerate(r):
                    item = QTableWidgetItem(str(v))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(i, c, item)

            # seçim reset
            self.selected_odunc = None

        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Aktif ödünçler yüklenemedi:\n{e}"
            )

    # ===============================
    # TABLE SELECT
    # ===============================
    def select_row(self, row, _):
        try:
            self.selected_odunc = int(
                self.table.item(row, 0).text()
            )
        except Exception:
            self.selected_odunc = None

    # ===============================
    # ACTION
    # ===============================
    def teslim_al(self):
        if not self.selected_odunc:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Lütfen teslim alınacak bir ödünç kaydı seçiniz."
            )
            return

        today = self.state.virtual_now.date()

        try:
            self.repo.teslim_al(self.selected_odunc, today)

            QMessageBox.information(
                self,
                "Başarılı",
                "Kitap teslim alma işlemi tamamlandı."
            )

            self.load_data()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Teslim Hatası",
                str(e)
            )
