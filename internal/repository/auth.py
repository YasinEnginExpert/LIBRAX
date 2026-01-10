class AuthRepository:
    def __init__(self, conn):
        self.conn = conn

    def login(self, username: str, password: str):
        """
        Kullanıcı giriş kontrolünü yapar.
        Kullanıcı adı ve şifre eşleşirse kullanıcı bilgilerini döndürür.
        Aksi halde None döner.
        """
        cur = self.conn.cursor()

        cur.execute(
            """
            SELECT kullaniciid, kullaniciadi, rol
            FROM kullanici
            WHERE kullaniciadi = %s
              AND sifre = %s
            """,
            (username, password)
        )

        return cur.fetchone()
