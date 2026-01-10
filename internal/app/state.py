from datetime import datetime, timedelta


class AppState:
    def __init__(self):
        self.session = None

        # Sanal zaman ofseti (gün)
        self._offset_days = 0

    @property
    def real_now(self):
        return datetime.now()

    @property
    def virtual_now(self):
        return self.real_now + timedelta(days=self._offset_days)

    def advance_days(self, days: int):
        if days <= 0:
            return
        self._offset_days += days


class Session:
    def __init__(self, kullanici_id, kullanici_adi, rol):
        self.kullanici_id = kullanici_id
        self.kullanici_adi = kullanici_adi
        self.rol = rol
