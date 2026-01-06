from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QMessageBox, QLabel
)
from internal.repository.uye import UyeRepository
from PySide6.QtCore import Qt


class UyeView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = UyeRepository(conn)
        self.on_back = on_back
        self.selected_id = None
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        root = QVBoxLayout()

        # ===== GERİ DÖN =====
        back_btn = QPushButton("← Geri Dön")
        back_btn.setFixedWidth(120)
        back_btn.setStyleSheet("font-weight:600;")
        back_btn.clicked.connect(self.on_back)
        root.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Arama
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ad / Soyad / Email ile ara")
        self.search_input.textChanged.connect(self.load_data)
        search_layout.addWidget(QLabel("Arama:"))
        search_layout.addWidget(self.search_input)
        root.addLayout(search_layout)

        # Tablo
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Ad", "Soyad", "Email", "Telefon", "Borç"]
        )
        self.table.cellClicked.connect(self.on_select)
        root.addWidget(self.table)

        # Form
        form = QHBoxLayout()
        self.ad = QLineEdit()
        self.soyad = QLineEdit()
        self.email = QLineEdit()
        self.telefon = QLineEdit()

        self.ad.setPlaceholderText("Ad")
        self.soyad.setPlaceholderText("Soyad")
        self.email.setPlaceholderText("Email")
        self.telefon.setPlaceholderText("Telefon")

        form.addWidget(self.ad)
        form.addWidget(self.soyad)
        form.addWidget(self.email)
        form.addWidget(self.telefon)
        root.addLayout(form)

        # Butonlar
        btns = QHBoxLayout()
        ekle_btn = QPushButton("Ekle")
        guncelle_btn = QPushButton("Güncelle")
        sil_btn = QPushButton("Sil")

        ekle_btn.clicked.connect(self.ekle)
        guncelle_btn.clicked.connect(self.guncelle)
        sil_btn.clicked.connect(self.sil)

        btns.addWidget(ekle_btn)
        btns.addWidget(guncelle_btn)
        btns.addWidget(sil_btn)
        root.addLayout(btns)

        self.setLayout(root)

    def load_data(self):
        keyword = self.search_input.text()
        rows = self.repo.listele(keyword)
        self.table.setRowCount(0)

        for r in rows:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for c, val in enumerate(r):
                self.table.setItem(row_idx, c, QTableWidgetItem(str(val)))

    def on_select(self, row, _):
        self.selected_id = int(self.table.item(row, 0).text())
        self.ad.setText(self.table.item(row, 1).text())
        self.soyad.setText(self.table.item(row, 2).text())
        self.email.setText(self.table.item(row, 3).text())
        self.telefon.setText(self.table.item(row, 4).text())

    def ekle(self):
        try:
            self.repo.ekle(
                self.ad.text(),
                self.soyad.text(),
                self.email.text(),
                self.telefon.text()
            )
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def guncelle(self):
        if not self.selected_id:
            return
        try:
            self.repo.guncelle(
                self.selected_id,
                self.ad.text(),
                self.soyad.text(),
                self.email.text(),
                self.telefon.text()
            )
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def sil(self):
        if not self.selected_id:
            return

        aktif_odunc, borc_var = self.repo.silinebilir_mi(self.selected_id)

        if aktif_odunc or borc_var:
            QMessageBox.warning(
                self,
                "Silme Engellendi",
                "Bu üyenin aktif ödünç kaydı veya borcu bulunduğu için"
                " silinemez."
            )
            return

        reply = QMessageBox.question(
            self,
            "Sil",
            "Bu üyeyi silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            self.repo.sil(self.selected_id)
            self.load_data()
        except Exception as e:
            # Trigger yine de yakalarsa
            QMessageBox.critical(
                self,
                "Silme Hatası",
                str(e)
            )