"""
sentetik_veri.py — Sentetik PostgreSQL çıktısı üreticisi

Akın'ın 16 tablolu şemasını temsil eden DataFrame'ler üretir.
Mehmet'in test_pipeline.py yaklaşımıyla tutarlı: n=100 hasta, bilinçli hatalar dahil.
Gerçek DB bağlantısı gerekmez.
"""

import random
import string
import uuid
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ──────────────────────────────────────────────────────────────────────────────
# Yardımcı fonksiyonlar
# ──────────────────────────────────────────────────────────────────────────────

def _random_date(start_year=2018, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 5, 1)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def _uuid():
    return str(uuid.uuid4())


def _patient_id(hasta_id: str) -> str:
    """UUID'yi pt_ formatına dönüştürür (ETL katmanı tarafından yapılacak işlem)."""
    return "pt_" + hasta_id.replace("-", "")[:8]


# ──────────────────────────────────────────────────────────────────────────────
# 1. hasta tablosu
# ──────────────────────────────────────────────────────────────────────────────

def make_hasta_df(n: int = 100) -> pd.DataFrame:
    """
    Akın'ın `hasta` tablosunu simüle eder.
    NOT: tc_kimlik_no dahil — ETL'nin bunu MongoDB'ye TAŞIMAMASI test edilecek.
    """
    genders = ["Erkek", "Kadın", "Bilinmiyor"]
    blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"]

    rows = []
    for _ in range(n):
        hasta_id = _uuid()
        rows.append({
            "hasta_id": hasta_id,
            "tc_kimlik_no": f"{random.randint(10000000000, 99999999999)}",  # PII — ETL temizlemeli
            "ad": f"Ad_{random.randint(1, 999)}",                           # PII — ETL temizlemeli
            "soyad": f"Soyad_{random.randint(1, 999)}",                    # PII — ETL temizlemeli
            "email": f"user{random.randint(1,9999)}@example.com",          # PII — ETL temizlemeli
            "telefon": f"05{random.randint(100000000, 999999999)}",        # PII — ETL temizlemeli
            "dogum_tarihi": _random_date(1950, 2005),
            "cinsiyet": random.choice(genders),
            "kan_grubu": random.choice(blood_types),
            "sehir": random.choice(["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"]),
        })

    df = pd.DataFrame(rows)

    # Bilinçli hata: %3 oranında dogum_tarihi null
    null_idx = df.sample(frac=0.03, random_state=SEED).index
    df.loc[null_idx, "dogum_tarihi"] = None

    return df


# ──────────────────────────────────────────────────────────────────────────────
# 2. lab_test + lab_sonuc joined
# ──────────────────────────────────────────────────────────────────────────────

def make_lab_df(hasta_df: pd.DataFrame, n: int = 300) -> pd.DataFrame:
    """
    `lab_test` + `lab_sonuc` join çıktısını simüle eder.
    Her satır bir hasta_id + parametre + ölçüm değeri.
    """
    loinc_params = [
        ("4548-4", "HbA1c", "%", 4.0, 5.6),
        ("8480-6", "Sistolik KB", "mmHg", 90.0, 120.0),
        ("8462-4", "Diastolik KB", "mmHg", 60.0, 80.0),
        ("2093-3", "Total Kolesterol", "mg/dL", 0.0, 200.0),
        ("2345-7", "Glukoz (Açlık)", "mg/dL", 70.0, 100.0),
        ("1751-7", "Albumin", "g/dL", 3.5, 5.0),
        ("2160-0", "Kreatinin", "mg/dL", 0.6, 1.2),
    ]

    hasta_ids = hasta_df["hasta_id"].tolist()
    rows = []

    for _ in range(n):
        hasta_id = random.choice(hasta_ids)
        loinc, name, unit, ref_min, ref_max = random.choice(loinc_params)
        # Normal dağılımda değer, zaman zaman aykırı
        ortalama = (ref_min + ref_max) / 2
        std = (ref_max - ref_min) / 4
        deger = round(float(np.random.normal(ortalama, std * 1.5)), 2)

        rows.append({
            "hasta_id": hasta_id,
            "loinc_kodu": loinc,
            "parametre_adi": name,
            "deger": deger,
            "birim": unit,
            "referans_min": ref_min,
            "referans_max": ref_max,
            "olcum_tarihi": _random_date(2024, 2026),
        })

    df = pd.DataFrame(rows)

    # Bilinçli hata: %5 oranında deger null
    null_idx = df.sample(frac=0.05, random_state=SEED).index
    df.loc[null_idx, "deger"] = None

    # Bilinçli hata: 2 satırda orphan hasta_id (hasta tablosunda yok)
    for i in range(2):
        df.iloc[i, df.columns.get_loc("hasta_id")] = "orphan_" + _uuid()[:8]

    return df


# ──────────────────────────────────────────────────────────────────────────────
# 3. tibbi_kayit + tani joined
# ──────────────────────────────────────────────────────────────────────────────

def make_tani_df(hasta_df: pd.DataFrame, n: int = 150) -> pd.DataFrame:
    """
    `tibbi_kayit` + `tani` join çıktısını simüle eder.
    aktif=False olanlar MongoDB'ye embed edilmemeli.
    """
    icd10_havuzu = [
        ("E11", "Type 2 Diabetes", "MEDIUM"),
        ("I10", "Essential Hypertension", "MEDIUM"),
        ("E78.0", "Hyperlipidemia", "LOW"),
        ("J45", "Asthma", "LOW"),
        ("M79.3", "Panniculitis", "LOW"),
        ("E66", "Obesity", "HIGH"),
        ("I25", "Chronic ischemic heart disease", "HIGH"),
        ("N18", "Chronic kidney disease", "HIGH"),
    ]

    hasta_ids = hasta_df["hasta_id"].tolist()
    rows = []

    for _ in range(n):
        hasta_id = random.choice(hasta_ids)
        icd10, tani_adi, siddet = random.choice(icd10_havuzu)
        rows.append({
            "hasta_id": hasta_id,
            "icd10_kodu": icd10,
            "tani_adi": tani_adi,
            "siddet": siddet,
            "aktif": random.random() > 0.25,   # %75 aktif
            "tani_tarihi": _random_date(2015, 2026),
            "kayit_turu": random.choice(["POLIKLINIK", "YATIS", "ACIL"]),
        })

    df = pd.DataFrame(rows)

    # Bilinçli hata: 3 satırda bozuk ICD-10 formatı (lowercase)
    bad_idx = df.sample(n=3, random_state=SEED).index
    df.loc[bad_idx, "icd10_kodu"] = df.loc[bad_idx, "icd10_kodu"].str.lower()

    return df


# ──────────────────────────────────────────────────────────────────────────────
# 4. genetik_profil + genetik_varyant joined
# ──────────────────────────────────────────────────────────────────────────────

def make_genetik_df(hasta_df: pd.DataFrame, n: int = 80) -> pd.DataFrame:
    """
    `genetik_profil` + `genetik_varyant` join çıktısını simüle eder.
    Sadece hastaların %60'ı genetik profil sahibi.
    """
    gen_havuzu = [
        ("BRCA1", "rs80357906", "PATHOGENIC", 0.85),
        ("BRCA2", "rs80358720", "PATHOGENIC", 0.80),
        ("TCF7L2", "rs7903146", "RISK_FACTOR", 0.40),
        ("APOE", "rs429358", "RISK_FACTOR", 0.35),
        ("MTHFR", "rs1801133", "LIKELY_BENIGN", 0.15),
        ("CFTR", "rs75527207", "VUS", 0.25),
    ]

    genetik_hastalar = hasta_df["hasta_id"].sample(
        frac=0.6, random_state=SEED
    ).tolist()

    rows = []
    for _ in range(n):
        hasta_id = random.choice(genetik_hastalar)
        gen, rsid, klinik_onemi, risk_skoru = random.choice(gen_havuzu)
        rows.append({
            "hasta_id": hasta_id,
            "gen_adi": gen,
            "rsid": rsid,
            "klinik_onemi": klinik_onemi,
            "risk_skoru": round(risk_skoru + random.uniform(-0.05, 0.05), 3),
            "analiz_turu": random.choice(["WES", "WGS", "SNP_PANEL"]),
            "analiz_tarihi": _random_date(2022, 2026),
        })

    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────────────
# 5. risk_degerlendirme + oneri joined
# ──────────────────────────────────────────────────────────────────────────────

def make_risk_df(hasta_df: pd.DataFrame, n: int = 100) -> pd.DataFrame:
    """
    `risk_degerlendirme` + `oneri` join çıktısını simüle eder.
    Her hasta birden fazla hastalık için risk değerlendirmesi alabilir.
    """
    hastaliklar = ["Type 2 Diabetes", "Cardiovascular Disease", "Breast Cancer", "CKD"]
    oneri_turleri = ["LIFESTYLE", "MEDICATION", "SCREENING", "REFERRAL"]

    hasta_ids = hasta_df["hasta_id"].tolist()
    rows = []

    for _ in range(n):
        hasta_id = random.choice(hasta_ids)
        hastalik = random.choice(hastaliklar)
        risk_skoru = round(random.uniform(0.05, 0.95), 3)

        if risk_skoru < 0.3:
            risk_kategorisi = "LOW"
        elif risk_skoru < 0.6:
            risk_kategorisi = "MEDIUM"
        elif risk_skoru < 0.8:
            risk_kategorisi = "HIGH"
        else:
            risk_kategorisi = "CRITICAL"

        rows.append({
            "hasta_id": hasta_id,
            "hastalik_adi": hastalik,
            "risk_skoru": risk_skoru,
            "risk_kategorisi": risk_kategorisi,
            "model_versiyonu": random.choice(["mdl_diabetes_v2", "mdl_cv_v1", "mdl_brca_v1"]),
            "hesaplama_tarihi": _random_date(2026, 2026),
            "oneri_turu": random.choice(oneri_turleri),
            "oneri_baslik": f"{hastalik} için {random.choice(oneri_turleri)} önerisi",
            "oneri_aciklama": "Detaylı açıklama buraya gelir.",
        })

    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────────────
# Tek çağrıda tüm veri setini döndür
# ──────────────────────────────────────────────────────────────────────────────

def make_all(n_hasta: int = 100) -> dict:
    """
    Tüm sentetik PostgreSQL çıktısını tek sözlük olarak döndürür.
    Kullanım: data = make_all(); df_hasta = data["hasta"]
    """
    hasta = make_hasta_df(n_hasta)
    return {
        "hasta": hasta,
        "lab": make_lab_df(hasta, n=n_hasta * 3),
        "tani": make_tani_df(hasta, n=int(n_hasta * 1.5)),
        "genetik": make_genetik_df(hasta, n=int(n_hasta * 0.8)),
        "risk": make_risk_df(hasta, n=n_hasta),
    }


if __name__ == "__main__":
    data = make_all()
    for name, df in data.items():
        print(f"  {name:10s}: {len(df):4d} satır, {len(df.columns)} sütun")
