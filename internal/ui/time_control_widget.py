from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QLabel, QMessageBox
)


class TimeControlWidget(QWidget):
    def __init__(self, conn, state):
        super().__init__()

        self.conn = conn
        self.state = state

        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout()

        label = QLabel("Zamanı İleri Al:")
        layout.addWidget(label)

        for days in (1, 7, 30):
            btn = QPushButton(f"+{days} gün")
            btn.clicked.connect(
                lambda _, d=days: self.advance_time(d)
            )
            layout.addWidget(btn)

        self.setLayout(layout)

    def advance_time(self, days: int):
        try:
            cur = self.conn.cursor()

            # Sanal sistem zamanını ilerlet
            cur.execute(
                """
                SELECT set_config(
                    'app.time_offset',
                    (current_setting('app.time_offset')::int + %s)::text,
                    false
                );
                """,
                (days,)
            )

            self.conn.commit()
            cur.close()

            # UI tarafındaki sanal zamanı da ilerlet
            self.state.advance_days(days)

            QMessageBox.information(
                self,
                "Zaman Güncellendi",
                f"Sistem zamanı {days} gün ileri alındı."
            )

        except Exception as e:
            self.conn.rollback()
            QMessageBox.critical(
                self,
                "Zaman Hatası",
                str(e)
            )
