from PySide6.QtCore import QObject, Signal
from dotenv import load_dotenv
import logging
import time

from internal.db.postgres import from_env, open_connection


class DBWorker(QObject):
    finished = Signal(object)
    error = Signal(str)

    def run(self):
        logging.info("=== DB WORKER STARTED ===")

        try:
            # .env yükle
            load_dotenv(".env")
            cfg = from_env()

            logging.info(
                "DB CONFIG → host=%s port=%s user=%s db=%s",
                cfg.get("host"),
                cfg.get("port"),
                cfg.get("user"),
                cfg.get("database")
            )

            # Simülasyon / loading UX
            time.sleep(1)

            # Bağlantı aç
            conn = open_connection(cfg)

            if not conn:
                raise RuntimeError("Veritabanı bağlantısı oluşturulamadı.")

            logging.info("  DB connection successful")

            self.finished.emit(conn)

        except Exception as e:
            logging.exception("DB connection failed")
            self.error.emit(str(e))

        finally:
            logging.info("=== DB WORKER FINISHED ===")
