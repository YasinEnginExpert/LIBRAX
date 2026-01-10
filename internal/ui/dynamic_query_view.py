from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QComboBox, QCheckBox,
    QPushButton, QSpinBox,
    QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from internal.repository.dinamik_kitap import DinamikKitapRepository


class DynamicQueryView(QWidget):
    def __init__(self, conn, on_back):
        super().__init__()
        self.repo = DinamikKitapRepository(conn)
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

        # ===== FİLTRELER =====
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

        # ===== ARA =====
        btn = QPushButton("Ara")
        btn.setMinimumHeight(36)
        btn.setStyleSheet("font-weight:600;")
        btn.clicked.connect(self.ara)
        root.addWidget(btn)

        # ===== TABLO =====
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Kitap", "Yazar",
            "Kategori", "Basım Yılı",
            "Toplam", "Mevcut"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)

        self.setLayout(root)

    # ===============================
    # ACTION
    # ===============================
    def ara(self):
        # Yıl mantık kontrolü
        yil_min = self.yil_min.value() or None
        yil_max = self.yil_max.value() or None

        if yil_min and yil_max and yil_min > yil_max:
            QMessageBox.warning(
                self,
                "Geçersiz Aralık",
                "Minimum basım yılı, maksimum basım yılından büyük olamaz."
            )
            return

        try:
            rows = self.repo.kitap_ara(
                kitap_adi=self.kitap_adi.text().strip() or None,
                yazar=self.yazar.text().strip() or None,
                yil_min=yil_min,
                yil_max=yil_max,
                sadece_mevcut=self.sadece_mevcut.isChecked(),
                order_by=self.order_by.currentText() or None,
                order_dir=self.order_dir.currentText()
            )

            self._fill_table(rows)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Sorgu Hatası",
                str(e)
            )

    # ===============================
    # TABLE HELPER
    # ===============================
    def _fill_table(self, rows):
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)
