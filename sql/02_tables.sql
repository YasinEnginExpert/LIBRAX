CREATE TABLE kullanici (
    kullaniciid SERIAL PRIMARY KEY,
    kullaniciadi VARCHAR(50) UNIQUE NOT NULL,
    sifre VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL
        CHECK (rol IN ('Admin', 'Gorevli'))
);


CREATE TABLE uye (
    uyeid SERIAL PRIMARY KEY,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefon VARCHAR(20),
    toplamborc NUMERIC(10,2) DEFAULT 0
);


CREATE TABLE kategori (
    kategoriid SERIAL PRIMARY KEY,
    kategoriadi VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE kitap (
    kitapid SERIAL PRIMARY KEY,
    kitapadi VARCHAR(150) NOT NULL,
    yazar VARCHAR(100) NOT NULL,
    yayinevi VARCHAR(100),
    basimyili INT,
    kategoriid INT NOT NULL,
    toplamadet INT NOT NULL CHECK (toplamadet >= 0),
    mevcutadet INT NOT NULL CHECK (mevcutadet >= 0),
    CHECK (mevcutadet <= toplamadet)
);


CREATE TABLE odunc (
    oduncid SERIAL PRIMARY KEY,
    uyeid INT NOT NULL,
    kitapid INT NOT NULL,
    gorevliid INT NOT NULL,
    odunctarihi DATE DEFAULT CURRENT_DATE NOT NULL,
    sonteslimtarihi DATE NOT NULL,
    teslimtarihi DATE
);


CREATE TABLE ceza (
    cezaid SERIAL PRIMARY KEY,
    uyeid INT NOT NULL,
    oduncid INT,
    tutar NUMERIC(10,2) NOT NULL CHECK (tutar > 0),
    cezatarihi DATE DEFAULT CURRENT_DATE NOT NULL
);



CREATE TABLE log_islem (
    logid SERIAL PRIMARY KEY,
    islemzamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    kullaniciid INT,
    tabloadi VARCHAR(50),
    islemturu VARCHAR(20),
    aciklama TEXT
);
