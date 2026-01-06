from datetime import datetime


class ProcRepository:
    def __init__(self, conn):
        """
        conn: psycopg2 connection
        """
        self.conn = conn

    # CALL sp_YeniOduncVer(p_UyeID, p_KitapID, p_GorevliID)
    def yeni_odunc_ver(self, uye_id: int, kitap_id: int, gorevli_id: int):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "CALL sp_YeniOduncVer(%s, %s, %s)",
                    (uye_id, kitap_id, gorevli_id),
                )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    # CALL sp_KitapTeslimAl(p_OduncID, p_TeslimTarihi)
    def kitap_teslim_al(self, odunc_id: int, teslim_tarihi: datetime):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "CALL sp_KitapTeslimAl(%s, %s)",
                    (odunc_id, teslim_tarihi),
                )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
