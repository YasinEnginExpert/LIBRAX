from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel,
    QMessageBox
)
from PySide6.QtCore import Qt
from internal.repository.odunc import OduncRepository


class OduncView(QWidget):
    def __init__(self, conn, state, on_back):
        super().__init__()
        self.repo = OduncRepository(conn)
        self.state = state
        self.on_back = on_back

        self.selected_uyeid = None
        self.selected_kitapid = None

        self._build_ui()
        self.load_uyeler()
        self.load_kitaplar()

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

        # ===== ÜST ALAN =====
        top = QHBoxLayout()

        # ---------- ÜYELER ----------
        left = QVBoxLayout()
        left.addWidget(QLabel("Üyeler"))

        self.uye_search = QLineEdit()
        self.uye_search.setPlaceholderText("Üye ara (ad / soyad)")
        self.uye_search.setClearButtonEnabled(True)
        self.uye_search.textChanged.connect(self.load_uyeler)
        left.addWidget(self.uye_search)

        self.uye_table = QTableWidget(0, 3)
        self.uye_table.setHorizontalHeaderLabels(
            ["ID", "Ad", "Soyad"]
        )
        self.uye_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.uye_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.uye_table.horizontalHeader().setStretchLastSection(True)
        self.uye_table.cellClicked.connect(self.on_uye_select)
        left.addWidget(self.uye_table)

        # ---------- KİTAPLAR ----------
        right = QVBoxLayout()
        right.addWidget(QLabel("Kitaplar"))

        self.kitap_search = QLineEdit()
        self.kitap_search.setPlaceholderText("Kitap ara (kitap adı)")
        self.kitap_search.setClearButtonEnabled(True)
        self.kitap_search.textChanged.connect(self.load_kitaplar)
        right.addWidget(self.kitap_search)

        self.kitap_table = QTableWidget(0, 3)
        self.kitap_table.setHorizontalHeaderLabels(
            ["ID", "Kitap", "Mevcut"]
        )
        self.kitap_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.kitap_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.kitap_table.horizontalHeader().setStretchLastSection(True)
        self.kitap_table.cellClicked.connect(self.on_kitap_select)
        right.addWidget(self.kitap_table)

        self.stok_label = QLabel("Mevcut Adet: -")
        self.stok_label.setStyleSheet("color:#6b7280;")
        right.addWidget(self.stok_label)

        top.addLayout(left, 1)
        top.addLayout(right, 1)
        root.addLayout(top)

        # ===== ÖDÜNÇ VER =====
        self.btn_odunc = QPushButton("Ödünç Ver")
        self.btn_odunc.setMinimumHeight(42)
        self.btn_odunc.setStyleSheet("font-weight:600;")
        self.btn_odunc.clicked.connect(self.odunc_ver)
        root.addWidget(self.btn_odunc)

        # ===== AKTİF ÖDÜNÇLER =====
        root.addWidget(QLabel(
            "Seçili Üyenin Aktif Ödünçleri (Teslim edilmemiş)"
        ))

        self.aktif_table = QTableWidget(0, 3)
        self.aktif_table.setHorizontalHeaderLabels(
            ["Kitap", "Ödünç Tarihi", "Son Teslim Tarihi"]
        )
        self.aktif_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.aktif_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.aktif_table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.aktif_table)

        self.setLayout(root)

    # ===============================
    # LOADERS
    # ===============================
    def load_uyeler(self):
        try:
            rows = self.repo.uyeler(
                self.uye_search.text().strip()
            )
            self.uye_table.setRowCount(len(rows))
            for i, r in enumerate(rows):
                for c, v in enumerate(r):
                    item = QTableWidgetItem(str(v))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.uye_table.setItem(i, c, item)

        except Exception as e:
            QMessageBox.critical(
                self, "Hata", f"Üyeler yüklenemedi:\n{e}"
            )

    def load_kitaplar(self):
        try:
            rows = self.repo.kitaplar(
                self.kitap_search.text().strip()
            )
            self.kitap_table.setRowCount(len(rows))
            for i, r in enumerate(rows):
                for c, v in enumerate(r):
                    item = QTableWidgetItem(str(v))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.kitap_table.setItem(i, c, item)

            self.selected_kitapid = None
            self.stok_label.setText("Mevcut Adet: -")

        except Exception as e:
            QMessageBox.critical(
                self, "Hata", f"Kitaplar yüklenemedi:\n{e}"
            )

    def load_aktif_oduncler(self):
        self.aktif_table.setRowCount(0)
        if not self.selected_uyeid:
            return

        try:
            rows = self.repo.aktif_oduncler(self.selected_uyeid)
            self.aktif_table.setRowCount(len(rows))
            for i, r in enumerate(rows):
                for c, v in enumerate(r):
                    self.aktif_table.setItem(
                        i, c, QTableWidgetItem(str(v))
                    )
        except Exception as e:
            QMessageBox.critical(
                self, "Hata", f"Aktif ödünçler yüklenemedi:\n{e}"
            )

    # ===============================
    # SELECT EVENTS
    # ===============================
    def on_uye_select(self, row, _):
        self.selected_uyeid = int(
            self.uye_table.item(row, 0).text()
        )
        self.load_aktif_oduncler()

    def on_kitap_select(self, row, _):
        self.selected_kitapid = int(
            self.kitap_table.item(row, 0).text()
        )
        mevcut = self.kitap_table.item(row, 2).text()
        self.stok_label.setText(f"Mevcut Adet: {mevcut}")

    # ===============================
    # ACTION
    # ===============================
    def odunc_ver(self):
        if not self.selected_uyeid or not self.selected_kitapid:
            QMessageBox.warning(
                self, "Uyarı", "Lütfen üye ve kitap seçiniz."
            )
            return

        if not self.state.session:
            QMessageBox.critical(
                self,
                "Hata",
                "Oturum bulunamadı. Lütfen tekrar giriş yapınız."
            )
            return

        kullanici_id = getattr(
            self.state.session, "kullanici_id", None
        )
        if kullanici_id is None:
            QMessageBox.critical(
                self,
                "Hata",
                "Session.kullanici_id bulunamadı."
            )
            return

        try:
            self.repo.odunc_ver(
                self.selected_uyeid,
                self.selected_kitapid,
                kullanici_id
            )

            QMessageBox.information(
                self,
                "Başarılı",
                "Ödünç verme işlemi başarıyla tamamlandı."
            )

            # refresh
            self.load_kitaplar()
            self.load_aktif_oduncler()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ödünç Verme Hatası",
                str(e)
            )
