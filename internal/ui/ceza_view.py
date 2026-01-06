from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTableWidget,
    QTableWidgetItem, QPushButton,
    QDateEdit
)
from PySide6.QtCore import QDate
from internal.repository.ceza import CezaRepository


class CezaView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = CezaRepository(conn)
        self.on_back = on_back

        self._build_ui()
        self.load_uyeler()
        self.load_data()

    def _build_ui(self):
        root = QVBoxLayout()

        # ===== Filtreler =====
        filters = QHBoxLayout()

        self.uye_combo = QComboBox()
        self.uye_combo.currentIndexChanged.connect(self.load_data)

        self.baslangic = QDateEdit()
        self.baslangic.setCalendarPopup(True)
        self.baslangic.setDate(QDate.currentDate().addMonths(-1))
        self.baslangic.dateChanged.connect(self.load_data)

        self.bitis = QDateEdit()
        self.bitis.setCalendarPopup(True)
        self.bitis.setDate(QDate.currentDate())
        self.bitis.dateChanged.connect(self.load_data)

        filters.addWidget(QLabel("Üye:"))
        filters.addWidget(self.uye_combo)
        filters.addWidget(QLabel("Başlangıç:"))
        filters.addWidget(self.baslangic)
        filters.addWidget(QLabel("Bitiş:"))
        filters.addWidget(self.bitis)

        root.addLayout(filters)

        # ===== Tablo =====
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Üye", "Tutar", "Tarih", "Ödünç ID"]
        )
        root.addWidget(self.table)

        # ===== Toplam Borç =====
        self.borc_label = QLabel("Toplam Borç: 0 TL")
        self.borc_label.setStyleSheet("font-weight:600;")
        root.addWidget(self.borc_label)

        # ===== Geri =====
        back_btn = QPushButton("Geri")
        back_btn.clicked.connect(self.on_back)
        root.addWidget(back_btn)

        self.setLayout(root)

    def load_uyeler(self):
        self.uye_combo.clear()
        self.uye_combo.addItem("Tümü", None)

        for uyeid, ad in self.repo.uyeleri_getir():
            self.uye_combo.addItem(ad, uyeid)

    def load_data(self):
        uyeid = self.uye_combo.currentData()
        bas = self.baslangic.date().toPython()
        bit = self.bitis.date().toPython()

        rows = self.repo.cezalari_getir(uyeid, bas, bit)

        self.table.setRowCount(0)
        for r in rows:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            for c, val in enumerate(r):
                self.table.setItem(
                    row_idx,
                    c,
                    QTableWidgetItem(str(val))
                )

        if uyeid:
            borc = self.repo.toplam_borc(uyeid)
            self.borc_label.setText(
                f"Toplam Borç: {borc} TL"
            )
        else:
            self.borc_label.setText("Toplam Borç: -")
