-- KITAP → KATEGORI
ALTER TABLE kitap
ADD CONSTRAINT fk_kitap_kategori
FOREIGN KEY (kategoriid)
REFERENCES kategori(kategoriid);

-- ODUNC
ALTER TABLE odunc
ADD CONSTRAINT fk_odunc_uye FOREIGN KEY (uyeid) REFERENCES uye(uyeid);

ALTER TABLE odunc
ADD CONSTRAINT fk_odunc_kitap FOREIGN KEY (kitapid) REFERENCES kitap(kitapid);

ALTER TABLE odunc
ADD CONSTRAINT fk_odunc_gorevli FOREIGN KEY (gorevliid) REFERENCES kullanici(kullaniciid);

-- CEZA
ALTER TABLE ceza
ADD CONSTRAINT fk_ceza_uye FOREIGN KEY (uyeid) REFERENCES uye(uyeid);

ALTER TABLE ceza
ADD CONSTRAINT fk_ceza_odunc FOREIGN KEY (oduncid) REFERENCES odunc(oduncid);

-- LOG
ALTER TABLE log_islem
ADD CONSTRAINT fk_log_kullanici
FOREIGN KEY (kullaniciid)
REFERENCES kullanici(kullaniciid)
ON DELETE SET NULL;
