from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem,
    QLabel, QDateEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from internal.repository.rapor import RaporRepository


class RaporlarView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = RaporRepository(conn)
        self.on_back = on_back

        self._build_ui()

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

        # ===== RAPOR SEÇİM =====
        top = QHBoxLayout()

        self.rapor_cb = QComboBox()
        self.rapor_cb.addItems([
            "Tarih Aralığına Göre Ödünçler",
            "Geciken Kitaplar",
            "En Çok Ödünç Alınan Kitaplar"
        ])

        self.baslangic = QDateEdit(
            QDate.currentDate().addMonths(-1)
        )
        self.baslangic.setCalendarPopup(True)

        self.bitis = QDateEdit(QDate.currentDate())
        self.bitis.setCalendarPopup(True)

        btn = QPushButton("Raporu Getir")
        btn.setMinimumHeight(36)
        btn.setStyleSheet("font-weight:600;")
        btn.clicked.connect(self.rapor_getir)

        top.addWidget(QLabel("Rapor:"))
        top.addWidget(self.rapor_cb)
        top.addWidget(QLabel("Başlangıç:"))
        top.addWidget(self.baslangic)
        top.addWidget(QLabel("Bitiş:"))
        top.addWidget(self.bitis)
        top.addWidget(btn)

        root.addLayout(top)

        # ===== TABLO =====
        self.table = QTableWidget(0, 0)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)

        self.setLayout(root)

    # ===============================
    # ACTION
    # ===============================
    def rapor_getir(self):
        rapor = self.rapor_cb.currentText()

        bas = self.baslangic.date().toPython()
        bit = self.bitis.date().toPython()

        # Tarih kontrolü
        if bas > bit:
            QMessageBox.warning(
                self,
                "Geçersiz Tarih",
                "Başlangıç tarihi, bitiş tarihinden büyük olamaz."
            )
            return

        try:
            if rapor == "Tarih Aralığına Göre Ödünçler":
                data = self.repo.odunc_tarih_raporu(bas, bit)
                headers = [
                    "Üye", "Kitap",
                    "Ödünç Tarihi",
                    "Teslim Tarihi",
                    "Durum"
                ]

            elif rapor == "Geciken Kitaplar":
                data = self.repo.geciken_kitaplar()
                headers = [
                    "Üye", "Kitap",
                    "Ödünç Tarihi",
                    "Son Teslim",
                    "Gecikme (Gün)"
                ]

            else:
                data = self.repo.en_cok_odunc_kitaplar(bas, bit)
                headers = [
                    "Kitap",
                    "Ödünç Sayısı"
                ]

            self._fill_table(headers, data)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Rapor Hatası",
                str(e)
            )

    # ===============================
    # TABLE HELPER
    # ===============================
    def _fill_table(self, headers, data):
        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(headers)

        for r, row in enumerate(data):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)
