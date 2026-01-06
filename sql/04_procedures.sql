-- =============================================
-- 04_procedures.sql
-- Stored Procedures
-- =============================================

CREATE OR REPLACE PROCEDURE public.sp_kitapteslimal(
    IN p_oduncid integer,
    IN p_teslimtarihi date
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_son_teslim DATE;
    v_uye_id INT;
    v_gecikme_gun INT;
    v_ceza_tutar NUMERIC(10,2);
BEGIN
    SELECT sonteslimtarihi, uyeid
    INTO v_son_teslim, v_uye_id
    FROM odunc
    WHERE oduncid = p_oduncid
      AND teslimtarihi IS NULL;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Geçersiz ödünç ID veya kitap zaten teslim edilmiş';
    END IF;

    UPDATE odunc
    SET teslimtarihi = p_teslimtarihi
    WHERE oduncid = p_oduncid;

    IF p_teslimtarihi > v_son_teslim THEN
        v_gecikme_gun := p_teslimtarihi - v_son_teslim;
        v_ceza_tutar := v_gecikme_gun * 5;

        INSERT INTO ceza (uyeid, oduncid, tutar, cezatarihi)
        VALUES (v_uye_id, p_oduncid, v_ceza_tutar, p_teslimtarihi);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE public.sp_uyeozetrapor(
    IN p_uyeid integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    SELECT
        u.uyeid,
        u.ad,
        u.soyad,
        COUNT(o.oduncid) AS toplamoduncsayisi,
        COUNT(CASE WHEN o.teslimtarihi IS NULL THEN 1 END) AS aktifoduncsayisi,
        COALESCE(SUM(c.tutar), 0) AS toplamcezatutari
    FROM uye u
    LEFT JOIN odunc o ON o.uyeid = u.uyeid
    LEFT JOIN ceza c ON c.uyeid = u.uyeid
    WHERE u.uyeid = p_uyeid
    GROUP BY u.uyeid, u.ad, u.soyad;
END;
$$;


CREATE OR REPLACE PROCEDURE public.sp_yenioduncver(
    IN p_uyeid integer,
    IN p_kitapid integer,
    IN p_gorevliid integer
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_aktif_odunc INT;
    v_mevcut_adet INT;
BEGIN
    SELECT COUNT(*) INTO v_aktif_odunc
    FROM odunc
    WHERE uyeid = p_uyeid
      AND teslimtarihi IS NULL;

    IF v_aktif_odunc >= 5 THEN
        RAISE EXCEPTION 'Üyenin aktif ödünç limiti dolu';
    END IF;

    SELECT mevcutadet INTO v_mevcut_adet
    FROM kitap
    WHERE kitapid = p_kitapid;

    IF v_mevcut_adet <= 0 THEN
        RAISE EXCEPTION 'Kitap stokta yok';
    END IF;

    INSERT INTO odunc (
        uyeid, kitapid, gorevliid,
        odunctarihi, sonteslimtarihi
    )
    VALUES (
        p_uyeid,
        p_kitapid,
        p_gorevliid,
        CURRENT_DATE,
        CURRENT_DATE + INTERVAL '15 day'
    );
END;
$$;
