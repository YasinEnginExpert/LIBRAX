-- =============================================
-- 04_procedures.sql
-- Stored Procedures
-- =============================================

CREATE OR REPLACE PROCEDURE sp_KitapTeslimAl(
    p_OduncID INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_kitapid INT;
BEGIN
    -- Aktif ödünç var mı?
    SELECT kitapid
    INTO v_kitapid
    FROM odunc
    WHERE oduncid = p_OduncID
      AND teslimtarihi IS NULL
    FOR UPDATE;

    IF v_kitapid IS NULL THEN
        RAISE EXCEPTION 'Geçerli bir aktif ödünç bulunamadı';
    END IF;

    -- Teslim al (SANAL TARİH)
    UPDATE odunc
    SET teslimtarihi = fn_bugun()
    WHERE oduncid = p_OduncID;

    -- Stok artır
    UPDATE kitap
    SET mevcutadet = mevcutadet + 1
    WHERE kitapid = v_kitapid;

END;
$$;


CREATE OR REPLACE PROCEDURE sp_uyeozetrapor(
    IN p_uyeid INT
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


CREATE OR REPLACE PROCEDURE sp_YeniOduncVer(
    p_UyeID INT,
    p_KitapID INT,
    p_GorevliID INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_mevcut INT;
BEGIN
    SELECT mevcutadet
    INTO v_mevcut
    FROM kitap
    WHERE kitapid = p_KitapID
    FOR UPDATE;

    IF v_mevcut IS NULL THEN
        RAISE EXCEPTION 'Kitap bulunamadı';
    END IF;

    IF v_mevcut <= 0 THEN
        RAISE EXCEPTION 'Bu kitabın stoğu yok';
    END IF;

    INSERT INTO odunc (
        uyeid,
        kitapid,
        gorevliid,
        odunctarihi,
        sonteslimtarihi
    )
    VALUES (
        p_UyeID,
        p_KitapID,
        p_GorevliID,
        fn_bugun(),
        fn_bugun() + INTERVAL '14 days'
    );

    UPDATE kitap
    SET mevcutadet = mevcutadet - 1
    WHERE kitapid = p_KitapID;
END;
$$;



CREATE OR REPLACE PROCEDURE sp_GecikmeleriKontrolEt()
LANGUAGE plpgsql
AS $$
DECLARE
    r RECORD;
    v_gecikme INT;
    v_ceza NUMERIC;
BEGIN
    FOR r IN
        SELECT
            o.oduncid,
            o.uyeid,
            o.sonteslimtarihi
        FROM odunc o
        WHERE o.teslimtarihi IS NULL
          AND fn_bugun() > o.sonteslimtarihi
    LOOP
        v_gecikme := fn_bugun() - r.sonteslimtarihi;
        v_ceza := v_gecikme * 2;

        -- Aynı ödünç için tekrar ceza yazma
        IF NOT EXISTS (
            SELECT 1 FROM ceza
            WHERE oduncid = r.oduncid
        ) THEN
            INSERT INTO ceza (
                uyeid,
                oduncid,
                tutar,
                cezatarihi
            )
            VALUES (
                r.uyeid,
                r.oduncid,
                v_ceza,
                fn_bugun()
            );

            UPDATE uye
            SET toplamborc = toplamborc + v_ceza
            WHERE uyeid = r.uyeid;
        END IF;
    END LOOP;
END;
$$;


