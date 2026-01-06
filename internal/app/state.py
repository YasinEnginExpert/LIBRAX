class AppState:
    def __init__(self):
        self.session = None


class Session:
    def __init__(self, kullanici_id, kullanici_adi, rol):
        self.kullanici_id = kullanici_id
        self.kullanici_adi = kullanici_adi
        self.rol = rol