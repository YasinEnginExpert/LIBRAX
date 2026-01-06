class DinamikKitapRepository:
    def __init__(self, conn):
        self.conn = conn

    def kitap_ara(
        self,
        kitap_adi=None,
        yazar=None,
        kategori_id=None,
        yil_min=None,
        yil_max=None,
        sadece_mevcut=False,
        order_by=None,
        order_dir="ASC"
    ):
        sql = """
        SELECT
            k.kitapid,
            k.kitapadi,
            k.yazar,
            kt.kategoriadi AS kategori,
            k.basimyili,
            k.toplamadet,
            k.mevcutadet
        FROM kitap k
        JOIN kategori kt ON kt.kategoriid = k.kategoriid
        """

        where_clauses = []
        params = []

        if kitap_adi:
            where_clauses.append("k.kitapadi ILIKE %s")
            params.append(f"%{kitap_adi}%")

        if yazar:
            where_clauses.append("k.yazar ILIKE %s")
            params.append(f"%{yazar}%")

        if kategori_id:
            where_clauses.append("k.kategoriid = %s")
            params.append(kategori_id)

        if yil_min and yil_min > 0:
            where_clauses.append("k.basimyili >= %s")
            params.append(yil_min)

        if yil_max and yil_max > 0:
            where_clauses.append("k.basimyili <= %s")
            params.append(yil_max)

        if sadece_mevcut:
            where_clauses.append("k.mevcutadet > 0")

        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        # ✅ ORDER BY whitelist (çok önemli)
        allowed_order_by = {
            "k.kitapadi",
            "k.yazar",
            "k.basimyili"
        }

        if order_by in allowed_order_by:
            order_dir = "DESC" if order_dir == "DESC" else "ASC"
            sql += f" ORDER BY {order_by} {order_dir}"

        cur = self.conn.cursor()
        try:
            cur.execute(sql, params)
            return cur.fetchall()
        except Exception:
            self.conn.rollback()
            raise
