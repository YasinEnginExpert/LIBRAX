from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel,
    QComboBox, QSpinBox, QMessageBox,
)
from PySide6.QtCore import Qt
from internal.repository.kitap import KitapRepository


class KitapView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = KitapRepository(conn)
        self.on_back = on_back
        self.selected_id = None

        self._build_ui()
        self.load_kategoriler()

        self.search_input.clear()
        self.load_data(force_all=True)

    # ===============================
    # UI OLUŞTUR
    # ===============================
    def _build_ui(self):
        root = QVBoxLayout()

        # ===== GERİ DÖN =====
        back_btn = QPushButton("← Geri Dön")
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(self.on_back)
        back_btn.setStyleSheet("font-weight:600;")
        root.addWidget(back_btn, alignment=Qt.AlignLeft)

        # ---- Arama ----
        search = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Kitap adı / Yazar ara")
        self.search_input.textChanged.connect(self.load_data)

        search.addWidget(QLabel("Arama:"))
        search.addWidget(self.search_input)
        root.addLayout(search)

        # ---- Tablo ----
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Kitap", "Yazar", "Kategori",
            "Yayınevi", "Basım Yılı",
            "Toplam", "Mevcut"
        ])
        self.table.cellClicked.connect(self.on_select)
        root.addWidget(self.table)

        # ---- Form ----
        form = QHBoxLayout()

        self.kitapadi = QLineEdit()
        self.yazar = QLineEdit()
        self.yayinevi = QLineEdit()

        self.kategori = QComboBox()

        self.basimyili = QSpinBox()
        self.basimyili.setRange(1500, 2100)

        self.toplamadet = QSpinBox()
        self.toplamadet.setRange(1, 1000)

        self.kitapadi.setPlaceholderText("Kitap Adı")
        self.yazar.setPlaceholderText("Yazar")
        self.yayinevi.setPlaceholderText("Yayınevi")

        form.addWidget(self.kitapadi)
        form.addWidget(self.yazar)
        form.addWidget(self.kategori)
        form.addWidget(self.yayinevi)
        form.addWidget(self.basimyili)
        form.addWidget(self.toplamadet)

        root.addLayout(form)

        # ---- Butonlar ----
        btns = QHBoxLayout()

        btn_ekle = QPushButton("Ekle")
        btn_guncelle = QPushButton("Güncelle")
        btn_sil = QPushButton("Sil")

        btn_ekle.clicked.connect(self.ekle)
        btn_guncelle.clicked.connect(self.guncelle)
        btn_sil.clicked.connect(self.sil)

        btns.addWidget(btn_ekle)
        btns.addWidget(btn_guncelle)
        btns.addWidget(btn_sil)

        root.addLayout(btns)
        self.setLayout(root)

    # ===============================
    # VERİ YÜKLE
    # ===============================
    def load_data(self, force_all=False):
        if force_all:
            rows = self.repo.listele(None)
        else:
            rows = self.repo.listele(self.search_input.text())

        self.table.setRowCount(0)
        for r in rows:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for c, val in enumerate(r):
                self.table.setItem(row_idx, c, QTableWidgetItem(str(val)))

    def load_kategoriler(self):
        self.kategori.clear()
        for kid, ad in self.repo.kategoriler():
            self.kategori.addItem(ad, kid)
    # ===============================
    # TABLO SEÇİM
    # ===============================

    def on_select(self, row, _):
        self.selected_id = int(self.table.item(row, 0).text())
        self.kitapadi.setText(self.table.item(row, 1).text())
        self.yazar.setText(self.table.item(row, 2).text())
        kategori_adi = self.table.item(row, 3).text()
        self.yayinevi.setText(self.table.item(row, 4).text())
        self.basimyili.setValue(int(self.table.item(row, 5).text()))
        self.toplamadet.setValue(int(self.table.item(row, 6).text()))

        for i in range(self.kategori.count()):
            if self.kategori.itemText(i) == kategori_adi:
                self.kategori.setCurrentIndex(i)
                break

    # ===============================
    # CRUD
    # ===============================
    def ekle(self):
        try:
            self.repo.ekle(
                self.kitapadi.text(),
                self.yazar.text(),
                self.kategori.currentData(),
                self.yayinevi.text(),
                self.basimyili.value(),
                self.toplamadet.value()
            )
            self.search_input.clear()
            self.load_data(force_all=True)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def guncelle(self):
        if not self.selected_id:
            return
        try:
            self.repo.guncelle(
                self.selected_id,
                self.kitapadi.text(),
                self.yazar.text(),
                self.kategori.currentData(),
                self.yayinevi.text(),
                self.basimyili.value(),
                self.toplamadet.value()
            )
            self.search_input.clear()
            self.load_data(force_all=True)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def sil(self):
        if not self.selected_id:
            return

        if self.repo.silinebilir_mi(self.selected_id):
            QMessageBox.warning(
                self,
                "Silme Engellendi",
                "Bu kitabın aktif ödünç kaydı bulunduğu için silinemez."
            )
            return

        if QMessageBox.question(
            self,
            "Sil",
            "Bu kitabı silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        ) != QMessageBox.Yes:
            return

        try:
            self.repo.sil(self.selected_id)
            self.search_input.clear()
            self.load_data(force_all=True)
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))
