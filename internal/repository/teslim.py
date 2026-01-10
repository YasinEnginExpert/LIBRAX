class TeslimRepository:
    def __init__(self, conn):
        self.conn = conn

    def aktif_oduncler(self, keyword=None):
        cur = self.conn.cursor()
        if keyword:
            cur.execute(
                """
                SELECT
                    o.oduncid,
                    u.ad || ' ' || u.soyad AS uye,
                    k.kitapadi,
                    o.odunctarihi,
                    o.sonteslimtarihi
                FROM odunc o
                JOIN uye u ON u.uyeid = o.uyeid
                JOIN kitap k ON k.kitapid = o.kitapid
                WHERE o.teslimtarihi IS NULL
                  AND (
                        u.ad ILIKE %s
                     OR u.soyad ILIKE %s
                     OR k.kitapadi ILIKE %s
                  )
                ORDER BY o.sonteslimtarihi
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            )
        else:
            cur.execute(
                """
                SELECT
                    o.oduncid,
                    u.ad || ' ' || u.soyad AS uye,
                    k.kitapadi,
                    o.odunctarihi,
                    o.sonteslimtarihi
                FROM odunc o
                JOIN uye u ON u.uyeid = o.uyeid
                JOIN kitap k ON k.kitapid = o.kitapid
                WHERE o.teslimtarihi IS NULL
                ORDER BY o.sonteslimtarihi
                """
            )
        return cur.fetchall()

    def teslim_al(self, oduncid, teslim_tarihi):
        cur = self.conn.cursor()
        cur.execute(
            "CALL sp_kitapteslimal(%s, %s)",
            (oduncid, teslim_tarihi)
        )
        self.conn.commit()
