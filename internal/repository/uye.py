class UyeRepository:
    def __init__(self, conn):
        self.conn = conn

    # ===============================
    # LISTELE
    # ===============================
    def listele(self, keyword=None):
        cur = self.conn.cursor()

        if keyword:
            cur.execute(
                """
                SELECT uyeid, ad, soyad, email, telefon, COALESCE(toplamborc, 0)
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
                SELECT uyeid, ad, soyad, email, telefon, COALESCE(toplamborc, 0)
                FROM uye
                ORDER BY ad, soyad
                """
            )

        return cur.fetchall()

    # ===============================
    # EKLE
    # ===============================
    def ekle(self, ad, soyad, email, telefon):
        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT INTO uye (ad, soyad, email, telefon, toplamborc)
            VALUES (%s, %s, %s, %s, 0)
            """,
            (ad, soyad, email, telefon)
        )

    # ===============================
    # GÜNCELLE
    # ===============================
    def guncelle(self, uyeid, ad, soyad, email, telefon):
        cur = self.conn.cursor()

        cur.execute(
            """
            UPDATE uye
            SET ad = %s,
                soyad = %s,
                email = %s,
                telefon = %s
            WHERE uyeid = %s
            """,
            (ad, soyad, email, telefon, uyeid)
        )

        if cur.rowcount == 0:
            raise Exception("Üye bulunamadı.")

    # ===============================
    # SİL
    # ===============================
    def sil(self, uyeid):
        cur = self.conn.cursor()

        cur.execute(
            "DELETE FROM uye WHERE uyeid = %s",
            (uyeid,)
        )

        if cur.rowcount == 0:
            raise Exception("Üye silinemedi veya bulunamadı.")

    # ===============================
    # SİLİNEBİLİR Mİ?
    # ===============================
    def silinebilir_mi(self, uyeid):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                EXISTS (SELECT 1 FROM odunc WHERE uyeid = %s) AS odunc_var,
                (SELECT toplamborc FROM uye WHERE uyeid = %s) > 0 AS borc_var
            """,
            (uyeid, uyeid)
        )
        return cur.fetchone()
