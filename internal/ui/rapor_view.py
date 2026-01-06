from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QDateEdit
)
from PySide6.QtCore import QDate
from internal.repository.rapor import RaporRepository


class RaporlarView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = RaporRepository(conn)
        self.on_back = on_back
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout()

        # Rapor seçimi
        top = QHBoxLayout()
        self.rapor_cb = QComboBox()
        self.rapor_cb.addItems([
            "Tarih Aralığına Göre Ödünçler",
            "Geciken Kitaplar",
            "En Çok Ödünç Alınan Kitaplar"
        ])

        self.baslangic = QDateEdit(QDate.currentDate().addMonths(-1))
        self.bitis = QDateEdit(QDate.currentDate())

        btn = QPushButton("Raporu Getir")
        btn.clicked.connect(self.rapor_getir)

        top.addWidget(QLabel("Rapor:"))
        top.addWidget(self.rapor_cb)
        top.addWidget(self.baslangic)
        top.addWidget(self.bitis)
        top.addWidget(btn)

        root.addLayout(top)

        # Tablo
        self.table = QTableWidget()
        root.addWidget(self.table)

        back = QPushButton("Geri")
        back.clicked.connect(self.on_back)
        root.addWidget(back)

        self.setLayout(root)

    def rapor_getir(self):
        rapor = self.rapor_cb.currentText()

        if rapor == "Tarih Aralığına Göre Ödünçler":
            data = self.repo.odunc_tarih_raporu(
                self.baslangic.date().toPython(),
                self.bitis.date().toPython()
            )
            headers = ["Üye", "Kitap", "Ödünç Tarihi",
                       "Teslim Tarihi", "Durum"]

        elif rapor == "Geciken Kitaplar":
            data = self.repo.geciken_kitaplar()
            headers = ["Üye", "Kitap", "Ödünç Tarihi",
                       "Son Teslim", "Gecikme (Gün)"]

        else:
            data = self.repo.en_cok_odunc_kitaplar(
                self.baslangic.date().toPython(),
                self.bitis.date().toPython()
            )
            headers = ["Kitap", "Ödünç Sayısı"]

        self.table.setRowCount(0)
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for row in data:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))
