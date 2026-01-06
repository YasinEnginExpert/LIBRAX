class UyeRepository:
    def __init__(self, conn):
        self.conn = conn

    def listele(self, keyword=None):
        cur = self.conn.cursor()
        if keyword:
            cur.execute(
                """
                SELECT uyeid, ad, soyad, email, telefon, toplamborc
                FROM uye
                WHERE ad ILIKE %s
                   OR soyad ILIKE %s
                   OR email ILIKE %s
                ORDER BY ad, soyad
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
            )
        else:
            cur.execute(
                """
                SELECT uyeid, ad, soyad, email, telefon, toplamborc
                FROM uye
                ORDER BY ad, soyad
                """
            )
        return cur.fetchall()

    def ekle(self, ad, soyad, email, telefon):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO uye (ad, soyad, email, telefon, toplamborc)
            VALUES (%s, %s, %s, %s, 0)
            """,
            (ad, soyad, email, telefon)
        )
        self.conn.commit()

    def guncelle(self, uyeid, ad, soyad, email, telefon):
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE uye
            SET ad=%s, soyad=%s, email=%s, telefon=%s
            WHERE uyeid=%s
            """,
            (ad, soyad, email, telefon, uyeid)
        )
        self.conn.commit()

    def sil(self, uyeid):
        cur = self.conn.cursor()
        cur.execute(
            "DELETE FROM uye WHERE uyeid=%s",
            (uyeid,)
        )
        self.conn.commit()

    def silinebilir_mi(self, uyeid):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                EXISTS (
                    SELECT 1 FROM odunc
                    WHERE uyeid = %s
                    AND teslimtarihi IS NULL
                ) AS aktif_odunc,
                (SELECT toplamborc FROM uye WHERE uyeid = %s) > 0 AS borc_var
            """,
            (uyeid, uyeid)
        )
        return cur.fetchone()
