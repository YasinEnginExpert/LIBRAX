from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTableWidget,
    QTableWidgetItem, QPushButton,
    QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate, Qt
from internal.repository.ceza import CezaRepository


class CezaView(QWidget):
    def __init__(self, conn, state, on_back):
        super().__init__()
        self.repo = CezaRepository(conn)
        self.state = state
        self.on_back = on_back

        self._build_ui()
        self._init_virtual_dates()
        self._load_uyeler_safe()
        self._load_data_safe()

    # ================= UI =================

    def _build_ui(self):
        root = QVBoxLayout()
        root.setSpacing(12)

        # ===== Filtreler =====
        filters = QHBoxLayout()

        self.uye_combo = QComboBox()
        self.uye_combo.currentIndexChanged.connect(self._load_data_safe)

        self.baslangic = QDateEdit(calendarPopup=True)
        self.baslangic.dateChanged.connect(self._load_data_safe)

        self.bitis = QDateEdit(calendarPopup=True)
        self.bitis.dateChanged.connect(self._load_data_safe)

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
            ["ID", "Üye", "Tutar (TL)", "Tarih", "Ödünç ID"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)

        # ===== Toplam Borç =====
        self.borc_label = QLabel("Toplam Borç: -")
        self.borc_label.setStyleSheet("font-weight:600;")
        root.addWidget(self.borc_label)

        # ===== Sanal Zaman Bilgisi =====
        virtual_label = QLabel(
            f"Sanal Bugün: {self.state.virtual_now.strftime('%d.%m.%Y')}"
        )
        virtual_label.setStyleSheet("color:gray; font-size:11px;")
        root.addWidget(virtual_label)

        # ===== Geri =====
        back_btn = QPushButton("Geri")
        back_btn.setMinimumHeight(36)
        back_btn.clicked.connect(self.on_back)
        root.addWidget(back_btn)

        self.setLayout(root)

    # ================= SANAL TARİH =================

    def _init_virtual_dates(self):
        virtual_today = QDate(
            self.state.virtual_now.year,
            self.state.virtual_now.month,
            self.state.virtual_now.day
        )

        self.baslangic.setDate(virtual_today.addMonths(-1))
        self.bitis.setDate(virtual_today)

    # ================= SAFE LOADERS =================

    def _load_uyeler_safe(self):
        try:
            self.uye_combo.blockSignals(True)
            self.uye_combo.clear()
            self.uye_combo.addItem("Tümü", None)

            for uyeid, ad in self.repo.uyeleri_getir():
                self.uye_combo.addItem(ad, uyeid)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Üyeler yüklenirken hata oluştu:\n{e}"
            )
        finally:
            self.uye_combo.blockSignals(False)

    def _load_data_safe(self):
        try:
            self._load_data()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Hata",
                f"Cezalar yüklenirken hata oluştu:\n{e}"
            )

    # ================= CORE LOGIC =================

    def _load_data(self):
        uyeid = self.uye_combo.currentData()
        bas = self.baslangic.date().toPython()
        bit = self.bitis.date().toPython()

        rows = self.repo.cezalari_getir(uyeid, bas, bit)

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

        # ===== Toplam Borç =====
        if uyeid:
            borc = self.repo.toplam_borc(uyeid)
            self.borc_label.setText(f"Toplam Borç: {borc} TL")
        else:
            self.borc_label.setText("Toplam Borç: -")
