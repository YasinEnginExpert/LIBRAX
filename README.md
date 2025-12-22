# LIBRAX
LIBRAX is a desktop-based library automation system that manages books, members, and borrowing relationships in a holistic and integrated manner within university libraries.

## ER Diagram (Crow’s Foot)

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
