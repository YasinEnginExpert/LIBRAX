import logging
from psycopg2 import Error as PGError


class OduncRepository:
    def __init__(self, conn):
        self.conn = conn

    # =========================
    # ÜYELER (liste + arama)
    # =========================
    def uyeler(self, keyword=None):
        kw = (keyword or "").strip()
        try:
            with self.conn.cursor() as cur:
                if kw:
                    like = f"%{kw}%"
                    cur.execute(
                        """
                        SELECT uyeid, ad, soyad
                        FROM uye
                        WHERE ad ILIKE %s
                           OR soyad ILIKE %s
                           OR (ad || ' ' || soyad) ILIKE %s
                        ORDER BY ad, soyad
                        """,
                        (like, like, like)
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
        except Exception:
            # SELECT'te rollback şart değil ama bağlantı state'i bozulduysa korur
            self.conn.rollback()
            raise

    # =========================
    # KİTAPLAR (liste + arama)
    # =========================
    def kitaplar(self, keyword=None, only_available=False):
        kw = (keyword or "").strip()
        try:
            with self.conn.cursor() as cur:
                if kw:
                    like = f"%{kw}%"
                    if only_available:
                        cur.execute(
                            """
                            SELECT kitapid, kitapadi, mevcutadet
                            FROM kitap
                            WHERE kitapadi ILIKE %s
                              AND mevcutadet > 0
                            ORDER BY kitapadi
                            """,
                            (like,)
                        )
                    else:
                        cur.execute(
                            """
                            SELECT kitapid, kitapadi, mevcutadet
                            FROM kitap
                            WHERE kitapadi ILIKE %s
                            ORDER BY kitapadi
                            """,
                            (like,)
                        )
                else:
                    if only_available:
                        cur.execute(
                            """
                            SELECT kitapid, kitapadi, mevcutadet
                            FROM kitap
                            WHERE mevcutadet > 0
                            ORDER BY kitapadi
                            """
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
        except Exception:
            self.conn.rollback()
            raise

    # =========================
    # SEÇİLİ ÜYENİN AKTİF ÖDÜNÇLERİ
    # =========================
    def aktif_oduncler(self, uyeid: int):
        try:
            with self.conn.cursor() as cur:
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
        except Exception:
            self.conn.rollback()
            raise

    # =========================
    # STORED PROCEDURE: sp_YeniOduncVer
    # =========================
    def odunc_ver(self, uyeid: int, kitapid: int, kullaniciid: int):
        """
        İş kuralı DB'de: sp_YeniOduncVer
        Burada sadece:
        - parametre doğrulama
        - transaction güvenliği
        - hata mesajını düzgün iletme
        """
        if not uyeid or not kitapid or not kullaniciid:
            raise ValueError("Üye / Kitap / Görevli bilgisi eksik.")

        try:
            logging.info(
                "CALL sp_YeniOduncVer(uye=%s, kitap=%s, gorevli=%s)",
                uyeid, kitapid, kullaniciid
            )

            with self.conn.cursor() as cur:
                # (Opsiyonel) hızlı varlık kontrolü: UI tutarsızlığını erkenden yakalar
                cur.execute("SELECT 1 FROM uye WHERE uyeid=%s", (uyeid,))
                if cur.fetchone() is None:
                    raise Exception("Seçilen üye artık bulunamadı (silinmiş olabilir).")

                cur.execute("SELECT mevcutadet FROM kitap WHERE kitapid=%s", (kitapid,))
                row = cur.fetchone()
                if row is None:
                    raise Exception("Seçilen kitap artık bulunamadı (silinmiş olabilir).")

                # Stok 0 ise prosedür zaten hata atabilir ama kullanıcıya daha net mesaj verelim
                if row[0] is not None and int(row[0]) <= 0:
                    raise Exception("Bu kitap stokta yok (mevcut adet = 0).")

                # Asıl iş kuralı prosedürde
                cur.execute(
                    "CALL sp_YeniOduncVer(%s, %s, %s)",
                    (uyeid, kitapid, kullaniciid)
                )

            self.conn.commit()
            logging.info("Ödünç verme başarılı.")
            return True

        except PGError as e:
            self.conn.rollback()
            # PostgreSQL RAISE EXCEPTION mesajı burada genelde e.diag.message_primary'de olur
            msg = getattr(getattr(e, "diag", None), "message_primary", None) or str(e)
            logging.error("PostgreSQL hata (ödünç): %s", msg)
            raise Exception(msg)

        except Exception as e:
            self.conn.rollback()
            logging.error("Ödünç verme hatası: %s", e)
            raise
