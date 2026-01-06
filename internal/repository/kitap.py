class KitapRepository:
    def __init__(self, conn):
        self.conn = conn

    # ===============================
    # KATEGORİLER (Combobox için)
    # ===============================
    def kategoriler(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT kategoriid, kategoriadi
            FROM kategori
            ORDER BY kategoriadi
            """
        )
        return cur.fetchall()

    # ===============================
    # KİTAP LİSTELE / ARA
    # ===============================
    def listele(self, keyword=None):
        cur = self.conn.cursor()

        if keyword:
            cur.execute(
                """
                SELECT
                    k.kitapid,
                    k.kitapadi,
                    k.yazar,
                    ka.kategoriadi,
                    k.yayinevi,
                    k.basimyili,
                    k.toplamadet,
                    k.mevcutadet
                FROM kitap k
                JOIN kategori ka ON ka.kategoriid = k.kategoriid
                WHERE k.kitapadi ILIKE %s
                   OR k.yazar ILIKE %s
                ORDER BY k.kitapadi
                """,
                (f"%{keyword}%", f"%{keyword}%")
            )
        else:
            cur.execute(
                """
                SELECT
                    k.kitapid,
                    k.kitapadi,
                    k.yazar,
                    ka.kategoriadi,
                    k.yayinevi,
                    k.basimyili,
                    k.toplamadet,
                    k.mevcutadet
                FROM kitap k
                JOIN kategori ka ON ka.kategoriid = k.kategoriid
                ORDER BY k.kitapadi
                """
            )

        return cur.fetchall()

    # ===============================
    # KİTAP EKLE
    # ===============================
    def ekle(
        self,
        kitapadi,
        yazar,
        kategoriid,
        yayinevi,
        basimyili,
        toplamadet
    ):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO kitap
            (kitapadi, yazar, kategoriid, yayinevi,
             basimyili, toplamadet, mevcutadet)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                kitapadi,
                yazar,
                kategoriid,
                yayinevi,
                basimyili,
                toplamadet,
                toplamadet
            )
        )
        self.conn.commit()

    # ===============================
    # KİTAP GÜNCELLE
    # ===============================
    def guncelle(
        self,
        kitapid,
        kitapadi,
        yazar,
        kategoriid,
        yayinevi,
        basimyili,
        toplamadet
    ):
        cur = self.conn.cursor()
        cur.execute(
            """
            UPDATE kitap
            SET kitapadi=%s,
                yazar=%s,
                kategoriid=%s,
                yayinevi=%s,
                basimyili=%s,
                toplamadet=%s
            WHERE kitapid=%s
            """,
            (
                kitapadi,
                yazar,
                kategoriid,
                yayinevi,
                basimyili,
                toplamadet,
                kitapid
            )
        )
        self.conn.commit()

    # ===============================
    # AKTİF ÖDÜNÇ VAR MI?
    # ===============================
    def silinebilir_mi(self, kitapid):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM odunc
                WHERE kitapid = %s
                  AND teslimtarihi IS NULL
            )
            """,
            (kitapid,)
        )
        return cur.fetchone()[0]

    # ===============================
    # KİTAP SİL
    # ===============================
    def sil(self, kitapid):
        cur = self.conn.cursor()
        cur.execute(
            "DELETE FROM kitap WHERE kitapid=%s",
            (kitapid,)
        )
        self.conn.commit()
