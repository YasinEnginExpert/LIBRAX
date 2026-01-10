import logging


def advance_time_and_check_penalty(conn, days: int):
    """
    Sistemin sanal zamanını ileri alır ve
    geciken ödünçler için ceza üretir.

    - days > 0 olmalı
    - Transaction güvenlidir
    """

    if days <= 0:
        raise ValueError("İleri alınacak gün sayısı 0'dan büyük olmalıdır.")

    cur = conn.cursor()

    try:
        logging.info("Zaman %s gün ileri alınıyor...", days)

        # Sanal zamanı ilerlet (SonTeslimTarihi geri çekilir)
        cur.execute(
            "CALL sp_ZamaniIlerle(%s);",
            (days,)
        )

        logging.info("Zaman ilerletildi")

        # 2️Geciken ödünçleri kontrol et → ceza üret
        cur.execute(
            "CALL sp_GecikmeleriKontrolEt();"
        )

        logging.info("Gecikme cezaları kontrol edildi")

        conn.commit()
        logging.info("Transaction commit edildi")

    except Exception as e:
        conn.rollback()
        logging.error(" Zaman ilerletme / ceza hatası: %s", e)
        raise e

    finally:
        cur.close()
