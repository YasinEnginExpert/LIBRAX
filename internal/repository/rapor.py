class RaporRepository:
    def __init__(self, conn):
        self.conn = conn

    # Tarih Aralığına Göre Ödünç Raporu
    def odunc_tarih_raporu(self, baslangic, bitis):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                u.ad || ' ' || u.soyad AS uye,
                k.kitapadi,
                o.odunctarihi,
                o.teslimtarihi,
                CASE
                    WHEN o.teslimtarihi IS NULL THEN 'Devam Ediyor'
                    ELSE 'Teslim Edildi'
                END AS durum
            FROM odunc o
            JOIN uye u ON u.uyeid = o.uyeid
            JOIN kitap k ON k.kitapid = o.kitapid
            WHERE o.odunctarihi BETWEEN %s AND %s
            ORDER BY o.odunctarihi DESC
            """,
            (baslangic, bitis)
        )
        return cur.fetchall()

    # Geciken Kitaplar Raporu
    def geciken_kitaplar(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                u.ad || ' ' || u.soyad AS uye,
                k.kitapadi,
                o.odunctarihi,
                o.sonteslimtarihi,
                (fn_bugun() - o.sonteslimtarihi) AS gecikme_gunu
            FROM odunc o
            JOIN uye u ON u.uyeid = o.uyeid
            JOIN kitap k ON k.kitapid = o.kitapid
            WHERE o.teslimtarihi IS NULL
            AND o.sonteslimtarihi <= fn_bugun()
            ORDER BY gecikme_gunu DESC
            """
        )
        return cur.fetchall()

    # En Çok Ödünç Alınan Kitaplar
    def en_cok_odunc_kitaplar(self, baslangic, bitis):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                k.kitapadi,
                COUNT(o.oduncid) AS odunc_sayisi
            FROM odunc o
            JOIN kitap k ON k.kitapid = o.kitapid
            WHERE o.odunctarihi BETWEEN %s AND %s
            GROUP BY k.kitapadi
            ORDER BY odunc_sayisi DESC
            """,
            (baslangic, bitis)
        )
        return cur.fetchall()

    def ceza_raporu(self, baslangic, bitis):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT
                u.ad || ' ' || u.soyad AS uye,
                k.kitapadi,
                c.tutar,
                c.cezatarihi
            FROM ceza c
            JOIN uye u ON u.uyeid = c.uyeid
            JOIN odunc o ON o.oduncid = c.oduncid
            JOIN kitap k ON k.kitapid = o.kitapid
            WHERE c.cezatarihi BETWEEN %s AND %s
            ORDER BY c.cezatarihi DESC
            """,
            (baslangic, bitis)
        )
        return cur.fetchall()