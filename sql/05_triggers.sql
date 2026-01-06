-- =============================================
-- 05_triggers.sql
-- Trigger Functions and Triggers
-- =============================================

CREATE OR REPLACE FUNCTION public.fn_ceza_insert()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE uye
    SET toplamborc = toplamborc + NEW.tutar
    WHERE uyeid = NEW.uyeid;

    INSERT INTO log_islem (
        kullaniciid, tabloadi, islemturu, aciklama
    )
    VALUES (
        NULL, 'CEZA', 'INSERT', 'Gecikme cezası eklendi'
    );

    RETURN NEW;
END;
$$;


CREATE OR REPLACE FUNCTION public.fn_odunc_insert()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE kitap
    SET mevcutadet = mevcutadet - 1
    WHERE kitapid = NEW.kitapid;

    INSERT INTO log_islem (
        kullaniciid, tabloadi, islemturu, aciklama
    )
    VALUES (
        NEW.gorevliid, 'ODUNC', 'INSERT', 'Yeni ödünç kaydı oluşturuldu'
    );

    RETURN NEW;
END;
$$;


CREATE OR REPLACE FUNCTION public.fn_odunc_update_teslim()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.teslimtarihi IS NULL AND NEW.teslimtarihi IS NOT NULL THEN
        UPDATE kitap
        SET mevcutadet = mevcutadet + 1
        WHERE kitapid = NEW.kitapid;

        INSERT INTO log_islem (
            kullaniciid, tabloadi, islemturu, aciklama
        )
        VALUES (
            NEW.gorevliid, 'ODUNC', 'UPDATE', 'Kitap teslim alındı'
        );
    END IF;
    RETURN NEW;
END;
$$;


CREATE OR REPLACE FUNCTION public.fn_uye_delete_block()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    v_aktif_odunc INT;
BEGIN
    SELECT COUNT(*) INTO v_aktif_odunc
    FROM odunc
    WHERE uyeid = OLD.uyeid
      AND teslimtarihi IS NULL;

    IF v_aktif_odunc > 0 THEN
        RAISE EXCEPTION 'Aktif ödüncü olan üye silinemez';
    END IF;

    IF OLD.toplamborc > 0 THEN
        RAISE EXCEPTION 'Borcu olan üye silinemez';
    END IF;

    RETURN OLD;
END;
$$;


CREATE TRIGGER tr_ceza_insert
AFTER INSERT ON ceza
FOR EACH ROW
EXECUTE FUNCTION public.fn_ceza_insert();


CREATE TRIGGER tr_odunc_insert
AFTER INSERT ON odunc
FOR EACH ROW
EXECUTE FUNCTION public.fn_odunc_insert();


CREATE TRIGGER tr_odunc_update_teslim
AFTER UPDATE ON odunc
FOR EACH ROW
EXECUTE FUNCTION public.fn_odunc_update_teslim();


CREATE TRIGGER tr_uye_delete_block
BEFORE DELETE ON uye
FOR EACH ROW
EXECUTE FUNCTION public.fn_uye_delete_block();
