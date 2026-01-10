import sys
import logging

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QMessageBox
)
from PySide6.QtCore import QTimer, QThread

from internal.app.state import AppState
from internal.services.db_worker import DBWorker

from internal.ui.login import LoginView
from internal.ui.dashboard import DashboardView
from internal.ui.placeholder import PlaceholderView
from internal.ui.loading import loading_screen

from internal.ui.uye_view import UyeView
from internal.ui.kitap_view import KitapView
from internal.ui.odunc_view import OduncView
from internal.ui.teslim_view import TeslimView
from internal.ui.ceza_view import CezaView
from internal.ui.rapor_view import RaporlarView
from internal.ui.dynamic_query_view import DynamicQueryView

from internal.repository.auth import AuthRepository


# ===============================
# LOGGING AYARI
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S"
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        logging.info("=== LIBRAX BOOTSTRAP START ===")

        self.conn = None
        self.state = AppState()

        self._setup_window()
        self._setup_statusbar()
        self._setup_clock()
        self._setup_db_thread()

    # ===========================
    # WINDOW
    # ===========================
    def _setup_window(self):
        self.setWindowTitle("LIBRAX")
        self.resize(900, 600)
        self.setCentralWidget(
            loading_screen("Veritabanına bağlanılıyor...")
        )

    # ===========================
    # STATUS BAR + CLOCK
    # ===========================
    def _setup_statusbar(self):
        self.status_label = QLabel()
        self.statusBar().addPermanentWidget(self.status_label)

    def _setup_clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

    def update_datetime(self):
        vtime = self.state.virtual_now
        self.status_label.setText(
            vtime.strftime("%d.%m.%Y  %H:%M:%S")
        )

    # ===========================
    # DB THREAD
    # ===========================
    def _setup_db_thread(self):
        self.thread = QThread(self)
        self.worker = DBWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_db_ready)
        self.worker.error.connect(self.on_db_error)

        self.thread.start()

    def on_db_ready(self, conn):
        if self.conn:
            logging.warning("DB already initialized, ignoring duplicate signal.")
            return

        self.conn = conn

        # ===============================
        # 1. ADIM: Sanal zaman ofsetini başlat
        # ===============================
        cur = self.conn.cursor()
        cur.execute(
            "SELECT set_config('app.time_offset', '0', false);"
        )
        self.conn.commit()
        cur.close()

        logging.info("Sanal zaman ofseti başlatıldı (app.time_offset = 0)")

        self.auth_repo = AuthRepository(conn)

        logging.info("DB hazır, login ekranı gösteriliyor.")
        self.show_login()

        self.thread.quit()
        self.thread.wait()

    def on_db_error(self, message: str):
        logging.error("DB connection failed: %s", message)

        QMessageBox.critical(
            self,
            "Veritabanı Hatası",
            f"Veritabanına bağlanılamadı:\n\n{message}"
        )

        self.close()

    # ===========================
    # NAVIGATION
    # ===========================
    def show_login(self):
        self.setCentralWidget(
            LoginView(
                self.state,
                self.auth_repo,
                self.show_dashboard
            )
        )

    def show_dashboard(self):
        self.setCentralWidget(
            DashboardView(
                self.state,
                self.conn,
                on_nav=self.navigate,
                on_logout=self.logout
            )
        )

    def navigate(self, key: str):
        pages = {
            "members": UyeView(self.conn, on_back=self.show_dashboard),
            "books": KitapView(self.conn, on_back=self.show_dashboard),
            "borrow": OduncView(self.conn, self.state, on_back=self.show_dashboard),
            "return": TeslimView(self.conn, self.state, on_back=self.show_dashboard),
            "penalties": CezaView(self.conn, self.state, on_back=self.show_dashboard),
            "reports": RaporlarView(self.conn, on_back=self.show_dashboard),
            "dynamic_query": DynamicQueryView(self.conn, on_back=self.show_dashboard),
        }

        self.setCentralWidget(
            pages.get(key, PlaceholderView("Sayfa bulunamadı", self.show_dashboard))
        )

    def logout(self):
        self.state.session = None
        self.show_login()

    # ===========================
    # CLEAN SHUTDOWN
    # ===========================
    def closeEvent(self, event):
        logging.info("Application closing...")

        try:
            if self.conn:
                self.conn.close()
                logging.info("DB connection closed.")
        except Exception as e:
            logging.warning("DB close error: %s", e)

        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        event.accept()


# ===============================
# APP ENTRY
# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
