
class CezaRepository:
    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CEZASI OLAN / OLABİLEN ÜYELER
    # =========================
    def uyeleri_getir(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT uyeid, ad || ' ' || soyad AS adsoyad
                    FROM uye
                    ORDER BY ad, soyad
                    """
                )
                return cur.fetchall()
        except Exception:
            self.conn.rollback()
            raise

    # =========================
    # CEZA LİSTESİ (FİLTRELİ)
    # =========================
    def cezalari_getir(self, uyeid=None, baslangic=None, bitis=None):
        try:
            with self.conn.cursor() as cur:
                query = """
                    SELECT
                        c.cezaid,
                        u.ad || ' ' || u.soyad AS uye,
                        c.tutar,
                        c.cezatarihi,
                        c.oduncid
                    FROM ceza c
                    JOIN uye u ON u.uyeid = c.uyeid
                """
                conditions = []
                params = []

                if uyeid:
                    conditions.append("c.uyeid = %s")
                    params.append(uyeid)

                if baslangic:
                    conditions.append("c.cezatarihi >= %s")
                    params.append(baslangic)

                if bitis:
                    conditions.append("c.cezatarihi <= %s")
                    params.append(bitis)

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                query += " ORDER BY c.cezatarihi DESC"

                cur.execute(query, params)
                return cur.fetchall()

        except Exception:
            self.conn.rollback()
            raise

    # =========================
    # TOPLAM BORÇ (GÜVENLİ)
    # =========================
    def toplam_borc(self, uyeid, verify=False):
        """
        verify=True:
            - CEZA tablosundan SUM alır
            - uye.toplamborc ile fark varsa loglar
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT toplamborc FROM uye WHERE uyeid = %s",
                    (uyeid,)
                )
                row = cur.fetchone()
                cache_borc = row[0] if row else 0

                if not verify:
                    return cache_borc

                cur.execute(
                    """
                    SELECT COALESCE(SUM(tutar), 0)
                    FROM ceza
                    WHERE uyeid = %s
                    """,
                    (uyeid,)
                )
                real_borc = cur.fetchone()[0]

                if verify and real_borc != cache_borc:
                    cur.execute(
                        "UPDATE uye SET toplamborc = %s WHERE uyeid = %s",
                        (real_borc, uyeid)
                    )

                return real_borc

        except Exception:
            self.conn.rollback()
            raise
