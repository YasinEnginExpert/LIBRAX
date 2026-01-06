from PySide6.QtCore import QObject, Signal
from dotenv import load_dotenv
import logging
import time

from internal.db.postgres import from_env, open_connection


class DBWorker(QObject):
    finished = Signal(object)  # SADECE conn

    def run(self):
        logging.info("DB thread started")

        load_dotenv(".env")
        cfg = from_env()

        logging.info(
            "DB CONFIG → host=%s user=%s db=%s",
            cfg["host"], cfg["user"], cfg["database"]
        )

        time.sleep(1)  # simülasyon

        conn = open_connection(cfg)

        logging.info("✅ DB connection successful")
        logging.info("DB thread finished")

        self.finished.emit(conn)
