class TeslimRepository:
    def __init__(self, conn):
        self.conn = conn

    # Aktif ödünçler
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

    # Stored procedure çağrısı
    def teslim_al(self, oduncid, tarih):
        cur = self.conn.cursor()
        cur.execute(
            "CALL sp_KitapTeslimAl(%s, %s)",
            (oduncid, tarih)
        )
        self.conn.commit()
