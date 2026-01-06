class CezaRepository:
    def __init__(self, conn):
        self.conn = conn

    def uyeleri_getir(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT uyeid, ad || ' ' || soyad
            FROM uye
            ORDER BY ad, soyad
            """
        )
        return cur.fetchall()

    def cezalari_getir(self, uyeid=None, baslangic=None, bitis=None):
        cur = self.conn.cursor()

        query = """
            SELECT
                c.cezaid,
                u.ad || ' ' || u.soyad AS uye,
                c.tutar,
                c.cezatarihi,
                c.oduncid
            FROM ceza c
            JOIN uye u ON u.uyeid = c.uyeid
            WHERE 1=1
        """
        params = []

        if uyeid:
            query += " AND c.uyeid = %s"
            params.append(uyeid)

        if baslangic:
            query += " AND c.cezatarihi >= %s"
            params.append(baslangic)

        if bitis:
            query += " AND c.cezatarihi <= %s"
            params.append(bitis)

        query += " ORDER BY c.cezatarihi DESC"

        cur.execute(query, params)
        return cur.fetchall()

    def toplam_borc(self, uyeid):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT toplamborc FROM uye WHERE uyeid = %s",
            (uyeid,)
        )
        row = cur.fetchone()
        return row[0] if row else 0
