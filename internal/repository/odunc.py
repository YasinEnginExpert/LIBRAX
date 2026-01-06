class OduncRepository:
    def __init__(self, conn):
        self.conn = conn

    # =========================
    # ÜYELER (liste + arama)
    # =========================
    def uyeler(self, keyword=None):
        cur = self.conn.cursor()
        if keyword and keyword.strip():
            cur.execute(
                """
                SELECT uyeid, ad, soyad
                FROM uye
                WHERE ad ILIKE %s
                   OR soyad ILIKE %s
                   OR (ad || ' ' || soyad) ILIKE %s
                ORDER BY ad, soyad
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            )
        else:
            cur.execute(
                """
                SELECT uyeid, ad, soyad
                FROM uye
                ORDER BY ad, soyad
                """
            )
        return cur.fetchall()

    # =========================
    # KİTAPLAR (liste + arama)
    # =========================
    def kitaplar(self, keyword=None):
        cur = self.conn.cursor()
        if keyword and keyword.strip():
            cur.execute(
                """
                SELECT kitapid, kitapadi, mevcutadet
                FROM kitap
                WHERE kitapadi ILIKE %s
                ORDER BY kitapadi
                """,
                (f"%{keyword}%",)
            )
        else:
            cur.execute(
                """
                SELECT kitapid, kitapadi, mevcutadet
                FROM kitap
                ORDER BY kitapadi
                """
            )
        return cur.fetchall()

    # =========================
    # SEÇİLİ ÜYENİN AKTİF ÖDÜNÇLERİ (BONUS)
    # =========================
    def aktif_oduncler(self, uyeid: int):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                k.kitapadi,
                o.odunctarihi,
                o.sonteslimtarihi
            FROM odunc o
            JOIN kitap k ON k.kitapid = o.kitapid
            WHERE o.uyeid = %s
              AND o.teslimtarihi IS NULL
            ORDER BY o.odunctarihi DESC
            """,
            (uyeid,)
        )
        return cur.fetchall()

    # =========================
    # STORED PROCEDURE: sp_YeniOduncVer
    # =========================
    def odunc_ver(self, uyeid: int, kitapid: int, kullaniciid: int):
        cur = self.conn.cursor()
        cur.execute(
            "CALL sp_YeniOduncVer(%s, %s, %s)",
            (uyeid, kitapid, kullaniciid)
        )
        self.conn.commit()
