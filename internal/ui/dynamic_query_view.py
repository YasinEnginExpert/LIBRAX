from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox,
    QCheckBox, QPushButton,
    QSpinBox, QTableWidget,
    QTableWidgetItem
)
from internal.repository.dinamik_kitap import DinamikKitapRepository


class DynamicQueryView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = DinamikKitapRepository(conn)
        self.on_back = on_back
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout()

        # ===== Filtreler =====
        f = QHBoxLayout()

        self.kitap_adi = QLineEdit()
        self.kitap_adi.setPlaceholderText("Kitap Adı")

        self.yazar = QLineEdit()
        self.yazar.setPlaceholderText("Yazar")

        self.yil_min = QSpinBox()
        self.yil_min.setRange(0, 2100)
        self.yil_min.setPrefix("Min: ")

        self.yil_max = QSpinBox()
        self.yil_max.setRange(0, 2100)
        self.yil_max.setPrefix("Max: ")

        self.sadece_mevcut = QCheckBox("Sadece mevcut kitaplar")

        self.order_by = QComboBox()
        self.order_by.addItems([
            "",
            "k.kitapadi",
            "k.yazar",
            "k.basimyili"
        ])

        self.order_dir = QComboBox()
        self.order_dir.addItems(["ASC", "DESC"])

        f.addWidget(self.kitap_adi)
        f.addWidget(self.yazar)
        f.addWidget(self.yil_min)
        f.addWidget(self.yil_max)
        f.addWidget(self.sadece_mevcut)
        f.addWidget(self.order_by)
        f.addWidget(self.order_dir)

        root.addLayout(f)

        # ===== Buton =====
        btn = QPushButton("Ara")
        btn.clicked.connect(self.ara)
        root.addWidget(btn)

        # ===== Tablo =====
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Kitap", "Yazar",
            "Kategori", "Basım Yılı",
            "Toplam", "Mevcut"
        ])
        root.addWidget(self.table)

        back = QPushButton("Geri")
        back.clicked.connect(self.on_back)
        root.addWidget(back)

        self.setLayout(root)

    def ara(self):
        rows = self.repo.kitap_ara(
            kitap_adi=self.kitap_adi.text() or None,
            yazar=self.yazar.text() or None,
            yil_min=self.yil_min.value() or None,
            yil_max=self.yil_max.value() or None,
            sadece_mevcut=self.sadece_mevcut.isChecked(),
            order_by=self.order_by.currentText() or None,
            order_dir=self.order_dir.currentText()
        )

        self.table.setRowCount(0)
        for row in rows:
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, val in enumerate(row):
                self.table.setItem(
                    r, c, QTableWidgetItem(str(val))
                )
