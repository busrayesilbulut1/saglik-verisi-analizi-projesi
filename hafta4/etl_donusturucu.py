"""

Akın'ın PostgreSQL şemasından (16 tablo) Sezer'in MongoDB şemasına (7 koleksiyon)
dönüşüm mantığını uygular. Gerçek DB bağlantısı yok; DataFrame alır, dict döner.

Hafta 3 ETL eşleştirme belgesi: Sezer/hafta3/02_etl_eslestirmesi.md
Hedef şema: Sezer/hafta3/03_sema_tasarimi.md
"""

import re
from datetime import datetime, timezone

import pandas as pd


# ──────────────────────────────────────────────────────────────────────────────
# Sabitler
# ──────────────────────────────────────────────────────────────────────────────

PII_FIELDS = {"tc_kimlik_no", "ad", "soyad", "email", "telefon"}
VALID_GENDERS = {"Erkek": "M", "Kadın": "F", "Bilinmiyor": "OTHER"}
VALID_BLOOD_TYPES = {"A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"}
VALID_RISK_LEVELS = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
VALID_CLINICAL_SIGNIFICANCE = {
    "PATHOGENIC", "LIKELY_PATHOGENIC", "VUS", "LIKELY_BENIGN", "BENIGN", "RISK_FACTOR"
}
ICD10_PATTERN = re.compile(r"^[A-Z][0-9]{2}(\.[0-9]{1,2})?$")
PATIENT_ID_PATTERN = re.compile(r"^pt_[a-z0-9]{8}$")

ETL_VERSION = "v1.0"


# ──────────────────────────────────────────────────────────────────────────────
# Yardımcı fonksiyonlar
# ──────────────────────────────────────────────────────────────────────────────

def _to_patient_id(hasta_id: str) -> str:
    """UUID'yi pt_ formatına çevirir."""
    return "pt_" + hasta_id.replace("-", "")[:8]


def _to_utc(dt: datetime | str | float | None) -> str | None:
    """Tarih değerini UTC ISO 8601 stringe çevirir."""
    if pd.isna(dt) or dt is None:
        return None
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            return None
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    return None


def _meta() -> dict:
    return {
        "source_db": "postgres_main",
        "etl_version": ETL_VERSION,
        "last_synced": datetime.now(timezone.utc).isoformat(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 1. patient_profile
# ──────────────────────────────────────────────────────────────────────────────

def transform_patient(
    hasta_row: pd.Series,
    tani_df: pd.DataFrame,
    risk_df: pd.DataFrame,
) -> dict:
    """
    `hasta` satırı + `tani` + `risk_degerlendirme` → patient_profile dokümanı.
    PII alanları (tc_kimlik_no, ad, soyad, email, telefon) dahil edilmez.
    """
    hasta_id = hasta_row["hasta_id"]
    patient_id = _to_patient_id(hasta_id)

    # Demografi — PII dışı
    dogum_tarihi = hasta_row.get("dogum_tarihi")
    birth_year = None
    if dogum_tarihi is not None and not (isinstance(dogum_tarihi, float) and pd.isna(dogum_tarihi)):
        try:
            if isinstance(dogum_tarihi, datetime):
                birth_year = int(dogum_tarihi.year)
            else:
                birth_year = int(pd.to_datetime(dogum_tarihi).year)
        except Exception:
            birth_year = None

    cinsiyet_raw = str(hasta_row.get("cinsiyet", "Bilinmiyor"))
    gender = VALID_GENDERS.get(cinsiyet_raw, "OTHER")

    kan_grubu = hasta_row.get("kan_grubu")
    blood_type = str(kan_grubu) if kan_grubu in VALID_BLOOD_TYPES else None

    # Kronik durumlar — sadece aktif tanılar
    hasta_tani = tani_df[tani_df["hasta_id"] == hasta_id].copy()
    aktif_tani = hasta_tani[hasta_tani["aktif"] == True]
    chronic_conditions = []
    for _, row in aktif_tani.iterrows():
        icd10 = str(row.get("icd10_kodu", "")).upper().strip()
        if ICD10_PATTERN.match(icd10):
            chronic_conditions.append({
                "icd10": icd10,
                "name": str(row.get("tani_adi", "")),
                "severity": str(row.get("siddet", "MEDIUM")),
                "diagnosed_at": _to_utc(row.get("tani_tarihi")),
            })

    # Risk skorları (hasta başına en son risk)
    hasta_risk = risk_df[risk_df["hasta_id"] == hasta_id]
    risk_scores = {}
    for hastalik, grp in hasta_risk.groupby("hastalik_adi"):
        latest = grp.sort_values("hesaplama_tarihi").iloc[-1]
        key = hastalik.lower().replace(" ", "_")
        risk_scores[key] = round(float(latest["risk_skoru"]), 4)

    # Referanslar
    refs = {
        "has_genetic_profile": False,  # transform_genetic çağrısından güncellenir
        "imaging_count": 0,
        "latest_assessment_id": None,
        "timeline_event_count": len(hasta_tani),
    }

    doc = {
        "patient_id": patient_id,
        "demographics": {
            "birth_year": birth_year,
            "gender": gender,
            "blood_type": blood_type,
            "city": hasta_row.get("sehir"),
        },
        "chronic_conditions": chronic_conditions,
        "allergies": [],
        "rollups": {
            "risk_scores": risk_scores,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        },
        "refs": refs,
        "meta": _meta(),
    }

    # PII kontrol: hiçbir PII alanı dokümana girmemeli
    for field in PII_FIELDS:
        assert field not in doc, f"PII alan sızdı: {field}"

    return doc


# ──────────────────────────────────────────────────────────────────────────────
# 2. lab_aggregates
# ──────────────────────────────────────────────────────────────────────────────

def compute_lab_aggregates(hasta_id: str, lab_df: pd.DataFrame) -> list[dict]:
    """
    `lab_test + lab_sonuc` → hasta başına parametre başına lab_aggregates dokümanları.
    Rollup pencereleri: 7g, 30g, 90g, 1y.
    """
    hasta_lab = lab_df[lab_df["hasta_id"] == hasta_id].copy()
    hasta_lab = hasta_lab.dropna(subset=["deger"])
    hasta_lab["olcum_tarihi"] = pd.to_datetime(hasta_lab["olcum_tarihi"], errors="coerce")

    now = pd.Timestamp.now(tz="UTC")
    # Timezone'suz timestamp'leri UTC kabul et
    if hasta_lab["olcum_tarihi"].dt.tz is None:
        hasta_lab["olcum_tarihi"] = hasta_lab["olcum_tarihi"].dt.tz_localize("UTC")

    docs = []
    for loinc, grp in hasta_lab.groupby("loinc_kodu"):
        grp = grp.sort_values("olcum_tarihi", ascending=False)
        latest_row = grp.iloc[0]
        ref_min = float(latest_row.get("referans_min", 0))
        ref_max = float(latest_row.get("referans_max", 0))
        latest_val = float(latest_row["deger"])

        def window_stats(days: int) -> dict:
            cutoff = now - pd.Timedelta(days=days)
            w = grp[grp["olcum_tarihi"] >= cutoff]["deger"].astype(float)
            if w.empty:
                return {"min": None, "max": None, "avg": None, "count": 0}
            return {
                "min": round(float(w.min()), 4),
                "max": round(float(w.max()), 4),
                "avg": round(float(w.mean()), 4),
                "count": int(w.count()),
            }

        docs.append({
            "patient_id": _to_patient_id(hasta_id),
            "parameter": {
                "code": loinc,
                "name": str(latest_row.get("parametre_adi", "")),
                "unit": str(latest_row.get("birim", "")),
                "reference_range": {"min": ref_min, "max": ref_max},
            },
            "windows": {
                "7d": window_stats(7),
                "30d": window_stats(30),
                "90d": window_stats(90),
                "1y": window_stats(365),
            },
            "latest": {
                "value": round(latest_val, 4),
                "measured_at": _to_utc(latest_row["olcum_tarihi"]),
                "is_abnormal": not (ref_min <= latest_val <= ref_max),
                "abnormal_direction": (
                    "HIGH" if latest_val > ref_max
                    else "LOW" if latest_val < ref_min
                    else None
                ),
            },
            "meta": _meta(),
        })

    return docs


# ──────────────────────────────────────────────────────────────────────────────
# 3. genetic_profile
# ──────────────────────────────────────────────────────────────────────────────

def transform_genetic(hasta_id: str, genetik_df: pd.DataFrame) -> dict | None:
    """
    `genetik_profil + genetik_varyant` → genetic_profile dokümanı.
    Hasta genetik veri yoksa None döner.
    """
    hasta_gen = genetik_df[genetik_df["hasta_id"] == hasta_id].copy()
    if hasta_gen.empty:
        return None

    variants = []
    pathogenic_count = 0
    for _, row in hasta_gen.iterrows():
        cs = str(row.get("klinik_onemi", "VUS"))
        if cs not in VALID_CLINICAL_SIGNIFICANCE:
            cs = "VUS"
        if cs == "PATHOGENIC":
            pathogenic_count += 1
        variants.append({
            "gene": str(row.get("gen_adi", "")),
            "rsid": str(row.get("rsid", "")),
            "clinical_significance": cs,
            "risk_score": round(float(row.get("risk_skoru", 0.0)), 4),
        })

    analiz_turu = str(hasta_gen.iloc[0].get("analiz_turu", "WES"))
    analiz_tarihi = _to_utc(hasta_gen.iloc[0].get("analiz_tarihi"))

    return {
        "patient_id": _to_patient_id(hasta_id),
        "analysis_type": analiz_turu,
        "analyzed_at": analiz_tarihi,
        "variants": variants,
        "rollups": {
            "clinically_significant_count": len(variants),
            "pathogenic_count": pathogenic_count,
            "vus_count": sum(1 for v in variants if v["clinical_significance"] == "VUS"),
        },
        "raw_file": {
            "hdfs_path": f"/data/genetic/{_to_patient_id(hasta_id)}/data.vcf.gz",
            "encryption_key_ref": f"kms:saglik/genetic/{_to_patient_id(hasta_id)}",
        },
        "meta": _meta(),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 4. risk_assessments
# ──────────────────────────────────────────────────────────────────────────────

def transform_risk(hasta_id: str, risk_df: pd.DataFrame) -> list[dict]:
    """
    `risk_degerlendirme + oneri` → risk_assessments dokümanları (hasta başına).
    """
    hasta_risk = risk_df[risk_df["hasta_id"] == hasta_id].copy()
    docs = []

    for idx, row in hasta_risk.iterrows():
        risk_skoru = float(row.get("risk_skoru", 0.0))
        risk_kategorisi = str(row.get("risk_kategorisi", "LOW"))
        if risk_kategorisi not in VALID_RISK_LEVELS:
            risk_kategorisi = "LOW"

        docs.append({
            "assessment_id": f"ras_{_to_patient_id(hasta_id)[3:]}_{idx:03d}",
            "patient_id": _to_patient_id(hasta_id),
            "disease": str(row.get("hastalik_adi", "")),
            "risk_score": round(risk_skoru, 4),
            "risk_level": risk_kategorisi,
            "model": {
                "id": str(row.get("model_versiyonu", "mdl_unknown")),
                "version": "1.0.0",
            },
            "recommendations": [
                {
                    "type": str(row.get("oneri_turu", "LIFESTYLE")),
                    "title": str(row.get("oneri_baslik", "")),
                    "description": str(row.get("oneri_aciklama", "")),
                }
            ],
            "computed_at": _to_utc(row.get("hesaplama_tarihi")),
            "meta": _meta(),
        })

    return docs


# ──────────────────────────────────────────────────────────────────────────────
# 5. Tam ETL çalıştırıcı (tüm hastaları işle)
# ──────────────────────────────────────────────────────────────────────────────

def run_etl(data: dict) -> dict:
    """
    Tüm sentetik veriyi ETL'den geçirir.
    Döndürülen dict: her koleksiyon için doküman listesi.
    """
    hasta_df = data["hasta"]
    lab_df = data["lab"]
    tani_df = data["tani"]
    genetik_df = data["genetik"]
    risk_df = data["risk"]

    patient_profiles = []
    lab_aggregates = []
    genetic_profiles = []
    risk_assessments = []

    for _, row in hasta_df.iterrows():
        hasta_id = row["hasta_id"]

        # patient_profile
        profile = transform_patient(row, tani_df, risk_df)
        patient_profiles.append(profile)

        # lab_aggregates
        lab_aggs = compute_lab_aggregates(hasta_id, lab_df)
        lab_aggregates.extend(lab_aggs)

        # genetic_profile
        gen_doc = transform_genetic(hasta_id, genetik_df)
        if gen_doc:
            genetic_profiles.append(gen_doc)
            # refs güncelle
            profile["refs"]["has_genetic_profile"] = True

        # risk_assessments
        risk_docs = transform_risk(hasta_id, risk_df)
        risk_assessments.extend(risk_docs)

    return {
        "patient_profile": patient_profiles,
        "lab_aggregates": lab_aggregates,
        "genetic_profile": genetic_profiles,
        "risk_assessments": risk_assessments,
    }
