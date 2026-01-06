[![LIBRAX Tanıtım Videosu](https://img.youtube.com/vi/XJAxeBnO2b8/hqdefault.jpg)](https://youtu.be/XJAxeBnO2b8)

# LIBRAX – Library Management System

LIBRAX, PostgreSQL tabanlı bir veritabanı ve Python (PySide6) kullanılarak geliştirilmiş,
masaüstü bir **Kütüphane Yönetim Sistemidir**.  
Üniversite kütüphanelerinde kitap, üye ve ödünç alma süreçlerini bütüncül ve entegre
bir şekilde yönetmeyi amaçlar.

Uygulama aşağıdaki temel işlevleri kapsar:

-  Üye yönetimi  
- Kitap ve kategori yönetimi  
- Ödünç alma – teslim işlemleri  
- Gecikme cezası hesaplama  
- Dinamik ve parametreli sorgulama  
- İşlem kayıtları (loglama)

---



## Kullanılan Teknolojiler

- Python 3.9+
- PostgreSQL 13+
- PySide6 (Qt for Python) – GUI
- psycopg2-binary – PostgreSQL bağlantısı
- python-dotenv – Ortam değişkenleri yönetimi

---

## Veritabanı Tasarımı (ER Diagram – Crow’s Foot)

```mermaid
erDiagram
    UYE ||--o{ ODUNC : "borrows"
    KITAP ||--o{ ODUNC : "is loaned in"
    KULLANICI ||--o{ ODUNC : "processes"
    KATEGORI ||--o{ KITAP : "categorizes"
    UYE ||--o{ CEZA : "receives"
    ODUNC ||--o| CEZA : "generates"

    KULLANICI o|--o{ LOG_ISLEM : "records"

    KULLANICI {
        int KullaniciID PK
        string KullaniciAdi
        string Sifre
        string Rol
    }

    UYE {
        int UyeID PK
        string Ad
        string Soyad
        string Email
        string Telefon
        decimal ToplamBorc
    }

    KATEGORI {
        int KategoriID PK
        string KategoriAdi
    }

    KITAP {
        int KitapID PK
        string KitapAdi
        string Yazar
        string Yayinevi
        int BasimYili
        int ToplamAdet
        int MevcutAdet
        int KategoriID FK
    }

    ODUNC {
        int OduncID PK
        int UyeID FK
        int KitapID FK
        int GorevliID FK
        date OduncTarihi
        date SonTeslimTarihi
        date TeslimTarihi
    }

    CEZA {
        int CezaID PK
        int UyeID FK
        int OduncID FK
        decimal Tutar
        date CezaTarihi
    }

    LOG_ISLEM {
        int LogID PK
        datetime IslemZamani
        int KullaniciID FK
        string TabloAdi
        string IslemTuru
        string Aciklama
    }
```

## 🗄️ Veritabanı Kurulumu

PostgreSQL üzerinde boş bir veritabanı oluşturun:

```sql
CREATE DATABASE librax;

\c librax
\i sql/01_schema.sql
\i sql/02_tables.sql
\i sql/03_constraints.sql
\i sql/04_procedures.sql
\i sql/05_triggers.sql
\i sql/06_sample_data.sql
```

## Ortam Değişkenleri (.env)

```sql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=librax
DB_SSLMODE=disable
```

## Python Ortamının Hazırlanması
```sql
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
pip install -r requirements.txt
python main.py
```






