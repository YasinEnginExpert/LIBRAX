import psycopg2
import os
import logging


def from_env():
    """
    Ortam değişkenlerinden PostgreSQL bağlantı ayarlarını alır.
    Eksik değişken varsa None dönebilir, bağlantı sırasında yakalanır.
    """
    return {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT", 5432)),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "sslmode": os.getenv("DB_SSLMODE", "disable"),
    }


def open_connection(cfg):
    """
    PostgreSQL bağlantısını açar.
    Hata durumunda açıklayıcı log üretir.
    """
    try:
        logging.info(
            "PostgreSQL bağlantısı deneniyor (%s@%s:%s/%s)",
            cfg.get("user"),
            cfg.get("host"),
            cfg.get("port"),
            cfg.get("database")
        )

        conn = psycopg2.connect(**cfg)

        # Otomatik commit (GUI uygulamalar için güvenli)
        conn.autocommit = True

        logging.info("PostgreSQL bağlantısı başarıyla kuruldu")
        return conn

    except psycopg2.OperationalError as e:
        logging.critical(
            "PostgreSQL bağlantı hatası: %s",
            e
        )
        raise

    except Exception as e:
        logging.critical(
            "Beklenmeyen DB hatası: %s",
            e
        )
        raise
