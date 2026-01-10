from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QLabel,
    QComboBox,
    QSpinBox,
    QMessageBox,
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
    # UI
    # ===============================
    def _build_ui(self):
        root = QVBoxLayout()
        root.setSpacing(12)

        # ===== GERİ =====
        back_btn = QPushButton("← Geri Dön")
        back_btn.setFixedWidth(120)
        back_btn.clicked.connect(self.on_back)
        back_btn.setStyleSheet("font-weight:600;")
        root.addWidget(back_btn, alignment=Qt.AlignLeft)

        # ===== ARAMA =====
        search = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Kitap adı / Yazar ara")
        self.search_input.textChanged.connect(self.load_data)

        search.addWidget(QLabel("Arama:"))
        search.addWidget(self.search_input)
        root.addLayout(search)

        # ===== TABLO =====
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Kitap",
                "Yazar",
                "Kategori",
                "Yayınevi",
                "Basım Yılı",
                "Toplam",
                "Mevcut",
            ]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellClicked.connect(self.on_select)
        root.addWidget(self.table)

        # ===== FORM =====
        form = QHBoxLayout()

        self.kitapadi = QLineEdit()
        self.kitapadi.setPlaceholderText("Kitap Adı")

        self.yazar = QLineEdit()
        self.yazar.setPlaceholderText("Yazar")

        self.kategori = QComboBox()

        self.yayinevi = QLineEdit()
        self.yayinevi.setPlaceholderText("Yayınevi")

        self.basimyili = QSpinBox()
        self.basimyili.setRange(1500, 2100)

        self.toplamadet = QSpinBox()
        self.toplamadet.setRange(1, 1000)

        form.addWidget(self.kitapadi)
        form.addWidget(self.yazar)
        form.addWidget(self.kategori)
        form.addWidget(self.yayinevi)
        form.addWidget(self.basimyili)
        form.addWidget(self.toplamadet)

        root.addLayout(form)

        # ===== BUTONLAR =====
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
    # DATA LOAD
    # ===============================
    def load_data(self, force_all=False):
        try:
            rows = self.repo.listele(None if force_all else self.search_input.text())

            self.table.setRowCount(len(rows))
            for row_idx, r in enumerate(rows):
                for c, val in enumerate(r):
                    item = QTableWidgetItem(str(val))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_idx, c, item)

            self.selected_id = None

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veriler yüklenemedi:\n{e}")

    def load_kategoriler(self):
        try:
            self.kategori.clear()
            for kid, ad in self.repo.kategoriler():
                self.kategori.addItem(ad, kid)
        except Exception as e:
            msg = f"Kategoriler yüklenemedi:\n{e}"
            QMessageBox.critical(self, "Hata", msg)

    # ===============================
    # TABLE SELECT
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
        if not self.kitapadi.text().strip() or not self.yazar.text().strip():
            QMessageBox.warning(
                self, "Eksik Bilgi", "Kitap adı ve yazar alanları zorunludur."
            )
            return

        try:
            self.repo.ekle(
                self.kitapadi.text().strip(),
                self.yazar.text().strip(),
                self.kategori.currentData(),
                self.yayinevi.text().strip(),
                self.basimyili.value(),
                self.toplamadet.value(),
            )
            self.search_input.clear()
            self.load_data(force_all=True)

        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def guncelle(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçiniz.")
            return

        try:
            # Kritik kontrol: Toplam >= Mevcut
            mevcut = self.repo.mevcut_adet(self.selected_id)
            if self.toplamadet.value() < mevcut:
                QMessageBox.warning(
                    self, "Geçersiz İşlem", "Toplam adet, mevcut adetten küçük olamaz."
                )
                return

            self.repo.guncelle(
                self.selected_id,
                self.kitapadi.text().strip(),
                self.yazar.text().strip(),
                self.kategori.currentData(),
                self.yayinevi.text().strip(),
                self.basimyili.value(),
                self.toplamadet.value(),
            )
            self.search_input.clear()
            self.load_data(force_all=True)

        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def sil(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kayıt seçiniz.")
            return

        if self.repo.silinebilir_mi(self.selected_id):
            QMessageBox.warning(
                self,
                "Silme Engellendi",
                "Bu kitabın aktif ödünç kaydı bulunduğu için silinemez.",
            )
            return

        if (
            QMessageBox.question(
                self,
                "Sil",
                "Bu kitabı silmek istediğinize emin misiniz?",
                QMessageBox.Yes | QMessageBox.No,
            )
            != QMessageBox.Yes
        ):
            return

        try:
            self.repo.sil(self.selected_id)
            self.search_input.clear()
            self.load_data(force_all=True)

        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    # ===============================
    #  MEVCUT ADET GETİR
    # ===============================
    def mevcut_adet(self, kitapid):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT mevcutadet
            FROM kitap
            WHERE kitapid = %s
            """,
            (kitapid,)
        )
        row = cur.fetchone()
        return row[0] if row else 0
