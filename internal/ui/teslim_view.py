from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel,
    QMessageBox
)
from PySide6.QtCore import Qt, QDate
from internal.repository.teslim import TeslimRepository


class TeslimView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = TeslimRepository(conn)
        self.on_back = on_back
        self.selected_odunc = None

        self._build_ui()
        self.load_data()

    def _build_ui(self):
        root = QVBoxLayout()

        # Geri dön
        back_btn = QPushButton("← Geri Dön")
        back_btn.clicked.connect(self.on_back)
        root.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Arama
        search_layout = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Üye / Kitap ara")
        self.search.textChanged.connect(self.load_data)
        search_layout.addWidget(QLabel("Arama:"))
        search_layout.addWidget(self.search)
        root.addLayout(search_layout)

        # Tablo
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Üye", "Kitap", "Ödünç Tarihi", "Son Teslim"]
        )
        self.table.cellClicked.connect(self.select_row)
        root.addWidget(self.table)

        # Teslim Al
        self.btn = QPushButton("Teslim Al")
        self.btn.setMinimumHeight(40)
        self.btn.clicked.connect(self.teslim_al)
        root.addWidget(self.btn)

        self.setLayout(root)

    def load_data(self):
        rows = self.repo.aktif_oduncler(self.search.text())
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            for c, v in enumerate(r):
                self.table.setItem(i, c, QTableWidgetItem(str(v)))

    def select_row(self, row, _):
        self.selected_odunc = int(self.table.item(row, 0).text())

    def teslim_al(self):
        if not self.selected_odunc:
            QMessageBox.warning(
                self,
                "Uyarı",
                "Lütfen bir ödünç kaydı seçin."
            )
            return

        today = QDate.currentDate().toString("yyyy-MM-dd")

        try:
            self.repo.teslim_al(self.selected_odunc, today)
            QMessageBox.information(
                self,
                "Başarılı",
                "Kitap teslim alındı."
            )
            self.load_data()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Teslim Hatası",
                str(e)
            )
