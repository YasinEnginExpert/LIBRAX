class KitapRepository:
    def __init__(self, conn):
        self.conn = conn

    # ===============================
    #  KATEGORİLER (Combobox)
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
    #  KİTAP LİSTELE / ARA
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
    #  KİTAP EKLE (AKILLI)
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
        try:
            #  Aynı kitap var mı kontrol et
            cur.execute(
                """
                SELECT kitapid
                FROM kitap
                WHERE kitapadi = %s
                  AND yazar = %s
                  AND kategoriid = %s
                  AND yayinevi = %s
                  AND basimyili = %s
                """,
                (kitapadi, yazar, kategoriid, yayinevi, basimyili)
            )

            row = cur.fetchone()

            if row:
                #  Varsa → adetleri artır
                kitapid = row[0]
                cur.execute(
                    """
                    UPDATE kitap
                    SET toplamadet = toplamadet + %s,
                        mevcutadet = mevcutadet + %s
                    WHERE kitapid = %s
                    """,
                    (toplamadet, toplamadet, kitapid)
                )
            else:
                #  Yoksa → yeni kayıt
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

        except Exception:
            self.conn.rollback()
            raise

    # ===============================
    #  KİTAP GÜNCELLE (KRİTİK)
    # ===============================
    def guncelle(
        self,
        kitapid,
        kitapadi,
        yazar,
        kategoriid,
        yayinevi,
        basimyili,
        yeni_toplamadet
    ):
        cur = self.conn.cursor()
        try:
            #  Mevcut stok bilgilerini al
            cur.execute(
                """
                SELECT toplamadet, mevcutadet
                FROM kitap
                WHERE kitapid = %s
                """,
                (kitapid,)
            )
            row = cur.fetchone()

            if not row:
                raise Exception("Kitap bulunamadı.")

            eski_toplamadet, eski_mevcutadet = row

            #  Toplam adet farkı
            fark = yeni_toplamadet - eski_toplamadet

            #  Yeni mevcutadet hesapla
            if fark > 0:
                #  Yeni kitap eklenmiş
                yeni_mevcutadet = eski_mevcutadet + fark
            else:
                #  Kitap azaltılmış → sınırla
                yeni_mevcutadet = min(eski_mevcutadet, yeni_toplamadet)

            #  Güncelle
            cur.execute(
                """
                UPDATE kitap
                SET kitapadi   = %s,
                    yazar      = %s,
                    kategoriid = %s,
                    yayinevi   = %s,
                    basimyili  = %s,
                    toplamadet = %s,
                    mevcutadet = %s
                WHERE kitapid = %s
                """,
                (
                    kitapadi,
                    yazar,
                    kategoriid,
                    yayinevi,
                    basimyili,
                    yeni_toplamadet,
                    yeni_mevcutadet,
                    kitapid
                )
            )

            self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise

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
    #  KİTAP SİL (KONTROLLÜ)
    # ===============================
    def sil(self, kitapid):
        cur = self.conn.cursor()
        try:
            # Önce aktif ödünç kontrolü yapılır
            if self.silinebilir_mi(kitapid):
                raise Exception(
                    "Bu kitaba ait ödünç kayıtları bulunduğu için silinemez."
                )

            # Silme işlemi
            cur.execute(
                "DELETE FROM kitap WHERE kitapid = %s",
                (kitapid,)
            )

            if cur.rowcount == 0:
                raise Exception("Kitap bulunamadı veya silinemedi.")

            self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise
    # ===============================
    #  MEVCUT ADET GETİR
    # ===============================

    def mevcut_adet(self, kitapid):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT mevcutadet
            FROM kitap
            WHERE kitapid = %s
            """,
            (kitapid,)
        )
        row = cur.fetchone()
        return row[0] if row else 0
