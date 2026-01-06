import psycopg2
import os


def from_env():
    return {
        "host": os.getenv("DB_HOST"),
        "port": int(os.getenv("DB_PORT")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME"),
        "sslmode": os.getenv("DB_SSLMODE"),
    }


def open_connection(cfg):
    return psycopg2.connect(**cfg)
