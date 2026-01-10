from datetime import datetime, date
import logging


class ProcRepository:
    def __init__(self, conn):
        """
        conn: psycopg2 connection
        """
        self.conn = conn

    # ===============================
    # YENİ ÖDÜNÇ VER
    # ===============================
    def yeni_odunc_ver(self, uye_id: int, kitap_id: int, gorevli_id: int):
        try:
            logging.info(
                "CALL sp_YeniOduncVer(uye=%s, kitap=%s, gorevli=%s)",
                uye_id, kitap_id, gorevli_id
            )

            with self.conn.cursor() as cur:
                cur.execute(
                    "CALL sp_YeniOduncVer(%s, %s, %s)",
                    (uye_id, kitap_id, gorevli_id),
                )

            self.conn.commit()
            logging.info("Ödünç verme başarılı.")

        except Exception as e:
            self.conn.rollback()
            logging.error("Ödünç verme hatası: %s", e)
            raise

    # ===============================
    # KİTAP TESLİM AL
    # ===============================
    def kitap_teslim_al(self, odunc_id: int, teslim_tarihi):
        """
        teslim_tarihi: datetime | date | str (yyyy-mm-dd)
        """

        # Tarih normalize et
        if isinstance(teslim_tarihi, date) and not isinstance(teslim_tarihi, datetime):
            teslim_tarihi = datetime.combine(teslim_tarihi, datetime.min.time())

        try:
            logging.info(
                "CALL sp_KitapTeslimAl(odunc=%s, tarih=%s)",
                odunc_id, teslim_tarihi
            )

            with self.conn.cursor() as cur:
                cur.execute(
                    "CALL sp_KitapTeslimAl(%s, %s)",
                    (odunc_id, teslim_tarihi),
                )

            self.conn.commit()
            logging.info("Teslim alma başarılı.")

        except Exception as e:
            self.conn.rollback()
            logging.error("Teslim alma hatası: %s", e)
            raise
