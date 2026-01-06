class UyeRepository:
    def __init__(self, conn):
        self.conn = conn

    def listele(self, keyword=None):
        cur = self.conn.cursor()
        try:
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

        except Exception as e:
            self.conn.rollback()
            raise e

    def ekle(self, ad, soyad, email, telefon):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO uye (ad, soyad, email, telefon, toplamborc)
                VALUES (%s, %s, %s, %s, 0)
                """,
                (ad, soyad, email, telefon)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def guncelle(self, uyeid, ad, soyad, email, telefon):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                UPDATE uye
                SET ad=%s, soyad=%s, email=%s, telefon=%s
                WHERE uyeid=%s
                """,
                (ad, soyad, email, telefon, uyeid)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def sil(self, uyeid):
        cur = self.conn.cursor()
        try:
            cur.execute(
                "DELETE FROM uye WHERE uyeid=%s",
                (uyeid,)
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def silinebilir_mi(self, uyeid):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """
                SELECT
                    EXISTS (
                        SELECT 1 FROM odunc
                        WHERE uyeid = %s
                          AND teslimtarihi IS NULL
                    ) AS aktif_odunc,
                    (SELECT toplamborc FROM uye WHERE uyeid = %s) > 0 AS
                    borc_var
                """,
                (uyeid, uyeid)
            )
            return cur.fetchone()

        except Exception as e:
            self.conn.rollback()
            raise e
