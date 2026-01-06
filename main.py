import sys
import logging
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QThread

from internal.app.state import AppState
from internal.ui.login import LoginView
from internal.ui.dashboard import DashboardView
from internal.ui.placeholder import PlaceholderView
from internal.ui.loading import loading_screen
from internal.services.db_worker import DBWorker
from internal.ui.uye_view import UyeView
from internal.repository.auth import AuthRepository
from internal.ui.kitap_view import KitapView
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, QDateTime
from internal.ui.teslim_view import TeslimView
from internal.ui.odunc_view import OduncView
from internal.ui.ceza_view import CezaView
from internal.ui.rapor_view import RaporlarView
from internal.ui.dynamic_query_view import DynamicQueryView


logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.status_label = QLabel()
        self.statusBar().addPermanentWidget(self.status_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

        logging.info("=== LIBRAX BOOTSTRAP START ===")

        self.setWindowTitle("LIBRAX")
        self.resize(900, 600)

        self.state = AppState()

        # Loading ekranı
        self.setCentralWidget(
            loading_screen("Veritabanına bağlanılıyor...")
        )

        # THREAD SETUP
        self.thread = QThread(self)
        self.worker = DBWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_db_ready)

        self.thread.start()

    def on_db_ready(self, conn):
        self.conn = conn
        self.auth_repo = AuthRepository(conn)
        self.show_login()

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
                on_nav=self.navigate,
                on_logout=self.logout
            )
        )

    def navigate(self, key: str):
        pages = {
            "members": UyeView(
                self.conn,
                on_back=self.show_dashboard
            ),
            "books": KitapView(
                self.conn,
                on_back=self.show_dashboard
            ),
            "borrow": OduncView(
                self.conn, self.state,
                on_back=self.show_dashboard
            ),
            "return": TeslimView(
                self.conn,
                on_back=self.show_dashboard
            ),
            "penalties": CezaView(
                self.conn,
                on_back=self.show_dashboard
            ),
            "reports": RaporlarView(
                self.conn,
                on_back=self.show_dashboard
            ),
            "dynamic_query": DynamicQueryView(
                self.conn,
                on_back=self.show_dashboard
            ),
        }

        page = pages.get(
            key,
            PlaceholderView("Sayfa bulunamadı", self.show_dashboard)
        )
        self.setCentralWidget(page)

    def logout(self):
        self.state.session = None
        self.show_login()

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.status_label.setText(
            now.toString("dd.MM.yyyy  HH:mm:ss")
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
