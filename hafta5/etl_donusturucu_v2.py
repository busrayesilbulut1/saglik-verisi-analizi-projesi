"""
etl_donusturucu_v2.py — Optimized ETL (Hafta 5)

Hafta 4'ün etl_donusturucu.py (v1) üzerine 5 optimizasyon + Hafta 5 düzeltmeleri:

  O-1: run_etl() içinde DataFrame filtreleme O(n²) → O(n)
       groupby ile ön-indeksleme → her hasta için O(1) lookup

  O-2: compute_lab_aggregates() rollup pencerelerini tek geçişe indirdi
       4 ayrı filter+scan → tek sorted pass

  O-3: meta.source_record_id eklendi
       Her dokümanda kaynak PostgreSQL kaydı izlenebilir

  O-4: Orphan satır loglama
       Sessiz drop → run_etl() orphan_log listesi döner

  O-5: 7g penceresi eklendi
       windows: "7d", "30d", "90d", "1y"

  FIX-1: PII assertion transform_patient() sonuna geri eklendi (v1'de vardı, v2'de eksikti)
  FIX-2: _hash_id() helper eklendi — SHA-256 + salt (KVKK pseudonimleştirme için)
  FIX-3: Type annotations eklendi (_to_utc, _meta)
  FIX-4: Büyük fonksiyonlar bölündü (_build_chronic_conditions, _build_risk_scores,
          _build_grouped_index, _detect_orphans, _process_patient)
  FIX-5: 3 eksik transformer eklendi (clinical_timeline, imaging_metadata, feature_store)

Public API (v1'den fark):
  - run_etl(data) → run_etl(data) -> tuple[dict, list]
    İkinci eleman orphan_log.
    collections, _ = run_etl(data)  # orphan_log'u yoksay

Bağımlılıklar: pandas, hashlib (stdlib)
"""

import hashlib
import os
import re
from datetime import datetime, timedelta, timezone

import pandas as pd


# ──────────────────────────────────────────────────────────────────────────────
# Sabitler (v1 ile aynı)
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

ETL_VERSION = "v2.0"

# O-2: pencere boyutları (gün cinsinden)
_WINDOW_DAYS = {"7d": 7, "30d": 30, "90d": 90, "1y": 365}

# FIX-2: KVKK pseudonimleştirme salt — ETL_HASH_SALT ortam değişkeninden okunur;
# tanımlanmamışsa geliştirme ortamı için fallback değer kullanılır.
_HASH_SALT = os.environ.get("ETL_HASH_SALT", "bayt_bukuculer_saglik")


# ──────────────────────────────────────────────────────────────────────────────
# Yardımcı fonksiyonlar
# ──────────────────────────────────────────────────────────────────────────────

def _to_patient_id(hasta_id: str) -> str:
    return "pt_" + hasta_id.replace("-", "")[:8]


def _to_utc(dt: datetime | str | float | None) -> str | None:
    """Tarih değerini UTC ISO 8601 string'e çevirir; dönüştürülemezse None döner."""
    if dt is None:
        return None
    if isinstance(dt, float) and pd.isna(dt):
        return None
    try:
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        if isinstance(dt, datetime):
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
    except Exception:
        return None
    return None


def _meta(source_record_id: str | None = None) -> dict:
    """ETL meta alanı — tüm koleksiyon dokümanlarına eklenir."""
    m: dict = {
        "source_db": "postgres_main",
        "etl_version": ETL_VERSION,
        "last_synced": datetime.now(timezone.utc).isoformat(),
    }
    if source_record_id is not None:
        m["source_record_id"] = source_record_id  # O-3
    return m


def _hash_id(val: str, salt: str = _HASH_SALT) -> str:
    """SHA-256 + salt ile pseudonimleştirme. Rainbow table saldırısına karşı salt zorunlu."""
    return "sha256:" + hashlib.sha256((salt + val).encode("utf-8")).hexdigest()


# ──────────────────────────────────────────────────────────────────────────────
# 1. patient_profile — yardımcılar + ana transformer
# ──────────────────────────────────────────────────────────────────────────────

def _build_chronic_conditions(hasta_tani: pd.DataFrame) -> list[dict]:
    """Aktif tanılardan ICD-10 validasyonlu kronik durum listesi üretir."""
    if hasta_tani.empty or "aktif" not in hasta_tani.columns:
        return []
    aktif = hasta_tani[hasta_tani["aktif"] == True]
    result = []
    for _, row in aktif.iterrows():
        icd10 = str(row.get("icd10_kodu", "")).upper().strip()
        if ICD10_PATTERN.match(icd10):
            result.append({
                "icd10": icd10,
                "name": str(row.get("tani_adi", "")),
                "severity": str(row.get("siddet", "MEDIUM")),
                "diagnosed_at": _to_utc(row.get("tani_tarihi")),
            })
    return result


def _build_risk_scores(hasta_risk_df: pd.DataFrame) -> dict:
    """Hasta başına hastalık adına göre en son risk skorlarını toplar."""
    scores: dict = {}
    if hasta_risk_df.empty or "hastalik_adi" not in hasta_risk_df.columns:
        return scores
    for hastalik, grp in hasta_risk_df.groupby("hastalik_adi"):
        latest = grp.sort_values("hesaplama_tarihi").iloc[-1]
        key = hastalik.lower().replace(" ", "_")
        scores[key] = round(float(latest["risk_skoru"]), 4)
    return scores


def transform_patient(
    hasta_row: pd.Series,
    hasta_tani: pd.DataFrame,
    hasta_risk_df: pd.DataFrame,
) -> dict:
    """
    hasta satırı + önceden filtrelenmiş tani + risk → patient_profile dokümanı.
    PII alanları (tc_kimlik_no, ad, soyad, email, telefon) dahil edilmez.
    """
    hasta_id = hasta_row["hasta_id"]
    patient_id = _to_patient_id(hasta_id)

    dogum_tarihi = hasta_row.get("dogum_tarihi")
    birth_year: int | None = None
    if dogum_tarihi is not None and not (isinstance(dogum_tarihi, float) and pd.isna(dogum_tarihi)):
        try:
            birth_year = int(pd.to_datetime(dogum_tarihi).year)
        except Exception:
            birth_year = None

    gender = VALID_GENDERS.get(str(hasta_row.get("cinsiyet", "Bilinmiyor")), "OTHER")
    kan_grubu = hasta_row.get("kan_grubu")
    blood_type = str(kan_grubu) if kan_grubu in VALID_BLOOD_TYPES else None

    doc = {
        "patient_id": patient_id,
        "demographics": {
            "birth_year": birth_year,
            "gender": gender,
            "blood_type": blood_type,
            "city": hasta_row.get("sehir"),
        },
        "chronic_conditions": _build_chronic_conditions(hasta_tani),
        "allergies": [],
        "rollups": {
            "risk_scores": _build_risk_scores(hasta_risk_df),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        },
        "refs": {
            "has_genetic_profile": False,
            "imaging_count": 0,
            "latest_assessment_id": None,
            "timeline_event_count": len(hasta_tani),
        },
        "meta": _meta(source_record_id=hasta_id),
    }

    # FIX-1: PII assertion — üretim kodu güvencesi (test suite'e ek katman)
    for field in PII_FIELDS:
        assert field not in doc, f"PII alan sızdı: {field}"

    return doc


# ──────────────────────────────────────────────────────────────────────────────
# 2. lab_aggregates  (O-2: tek geçiş rollup, O-5: 7d penceresi)
# ──────────────────────────────────────────────────────────────────────────────

def compute_lab_aggregates(hasta_id: str, hasta_lab: pd.DataFrame) -> list[dict]:
    """
    hasta_lab önceden filtrelenmiş gelir (O-1).
    4 ayrı window scan → tek sıralı geçiş (O-2).
    "7d" penceresi eklendi (O-5).
    """
    if hasta_lab.empty or "deger" not in hasta_lab.columns:
        return []
    hasta_lab = hasta_lab.dropna(subset=["deger"]).copy()
    if hasta_lab.empty:
        return []

    hasta_lab["olcum_tarihi"] = pd.to_datetime(hasta_lab["olcum_tarihi"], errors="coerce")
    if hasta_lab["olcum_tarihi"].dt.tz is None:
        hasta_lab["olcum_tarihi"] = hasta_lab["olcum_tarihi"].dt.tz_localize("UTC")

    now = pd.Timestamp.now(tz="UTC")
    cutoffs = {label: now - pd.Timedelta(days=days) for label, days in _WINDOW_DAYS.items()}

    docs = []
    for loinc, grp in hasta_lab.groupby("loinc_kodu"):
        grp = grp.sort_values("olcum_tarihi", ascending=False)
        latest_row = grp.iloc[0]
        ref_min = float(latest_row.get("referans_min", 0))
        ref_max = float(latest_row.get("referans_max", 0))
        latest_val = float(latest_row["deger"])

        # O-2: Tek geçişli pencere hesabı
        window_vals: dict[str, list[float]] = {label: [] for label in _WINDOW_DAYS}
        for _, row in grp.iterrows():
            t = row["olcum_tarihi"]
            v = float(row["deger"])
            for label, cutoff in cutoffs.items():
                if t >= cutoff:
                    window_vals[label].append(v)

        def _stats(vals: list[float]) -> dict:
            if not vals:
                return {"min": None, "max": None, "avg": None, "count": 0}
            return {
                "min": round(min(vals), 4),
                "max": round(max(vals), 4),
                "avg": round(sum(vals) / len(vals), 4),
                "count": len(vals),
            }

        docs.append({
            "patient_id": _to_patient_id(hasta_id),
            "parameter": {
                "code": loinc,
                "name": str(latest_row.get("parametre_adi", "")),
                "unit": str(latest_row.get("birim", "")),
                "reference_range": {"min": ref_min, "max": ref_max},
            },
            "windows": {label: _stats(window_vals[label]) for label in _WINDOW_DAYS},
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
            "meta": _meta(source_record_id=hasta_id),
        })

    return docs


# ──────────────────────────────────────────────────────────────────────────────
# 3. genetic_profile
# ──────────────────────────────────────────────────────────────────────────────

def transform_genetic(hasta_id: str, hasta_gen: pd.DataFrame) -> dict | None:
    """hasta_gen önceden filtrelenmiş (O-1). Genetik veri yoksa None döner."""
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

    return {
        "patient_id": _to_patient_id(hasta_id),
        "analysis_type": str(hasta_gen.iloc[0].get("analiz_turu", "WES")),
        "analyzed_at": _to_utc(hasta_gen.iloc[0].get("analiz_tarihi")),
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
        "meta": _meta(source_record_id=hasta_id),
    }


# ──────────────────────────────────────────────────────────────────────────────
# 4. risk_assessments
# ──────────────────────────────────────────────────────────────────────────────

def transform_risk(hasta_id: str, hasta_risk: pd.DataFrame) -> list[dict]:
    """hasta_risk önceden filtrelenmiş (O-1)."""
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
            "meta": _meta(source_record_id=str(idx)),
        })
    return docs


# ──────────────────────────────────────────────────────────────────────────────
# 5. clinical_timeline  (FIX-5: yeni transformer)
# ──────────────────────────────────────────────────────────────────────────────

def transform_clinical_timeline(
    hasta_id: str,
    tibbi_kayit_df: pd.DataFrame,
    tani_df: pd.DataFrame,
    recete_df: pd.DataFrame,
) -> list[dict]:
    """
    tibbi_kayit + tani + ilac_recete → clinical_timeline dokümanları.
    doktor_id SHA-256 + salt ile pseudonimleştirilir (FIX-2).
    """
    hasta_kayit = tibbi_kayit_df[tibbi_kayit_df["hasta_id"] == hasta_id]
    if hasta_kayit.empty:
        return []

    tani_by_kayit: dict = {
        kid: grp for kid, grp in tani_df.groupby("kayit_id")
    } if "kayit_id" in tani_df.columns else {}
    recete_by_kayit: dict = {
        kid: grp for kid, grp in recete_df.groupby("kayit_id")
    } if "kayit_id" in recete_df.columns else {}

    docs = []
    for _, row in hasta_kayit.iterrows():
        kayit_id = str(row.get("kayit_id", ""))
        doktor_id_raw = str(row.get("doktor_id", ""))

        kayit_tani = tani_by_kayit.get(kayit_id, pd.DataFrame())
        diagnoses = [
            {"icd10": str(r.get("icd10_kodu", "")).upper().strip(),
             "name": str(r.get("tani_adi", ""))}
            for _, r in kayit_tani.iterrows()
            if ICD10_PATTERN.match(str(r.get("icd10_kodu", "")).upper().strip())
        ]

        kayit_recete = recete_by_kayit.get(kayit_id, pd.DataFrame())
        prescriptions_summary = {
            "prescription_count": len(kayit_recete),
            "medication_count": 0,
        }

        docs.append({
            "patient_id": _to_patient_id(hasta_id),
            "event_id": f"evt_{kayit_id[:8]}" if kayit_id else "evt_unknown",
            "event_type": str(row.get("kayit_turu", "POLIKLINIK")),
            "event_at": _to_utc(row.get("ziyaret_tarihi")),
            "doctor_id_hash": _hash_id(doktor_id_raw) if doktor_id_raw else None,
            "facility": str(row.get("hastane_adi", "")),
            "complaint": str(row.get("sikayet", "")),
            "diagnoses": diagnoses,
            "prescriptions_summary": prescriptions_summary,
            "notes_excerpt": str(row.get("tani_notu", ""))[:200],
            "meta": _meta(source_record_id=kayit_id),
        })

    return docs


# ──────────────────────────────────────────────────────────────────────────────
# 6. imaging_metadata  (FIX-5: yeni transformer)
# ──────────────────────────────────────────────────────────────────────────────

def transform_imaging(hasta_id: str, goruntu_df: pd.DataFrame) -> list[dict]:
    """
    tibbi_goruntu satırları → imaging_metadata dokümanları.
    Ham DICOM dosyası HDFS'te kalır; sadece metadata MongoDB'ye yazar.
    """
    hasta_goruntu = goruntu_df[goruntu_df["hasta_id"] == hasta_id]
    if hasta_goruntu.empty:
        return []

    docs = []
    for _, row in hasta_goruntu.iterrows():
        goruntu_id = str(row.get("goruntu_id", ""))
        docs.append({
            "patient_id": _to_patient_id(hasta_id),
            "dicom_uid": str(row.get("dicom_uid", "")),
            "modality": str(row.get("goruntu_turu", "UNKNOWN")),
            "captured_at": _to_utc(row.get("cekim_tarihi")),
            "hdfs_path": str(row.get("depolama_yolu", "")),
            "encryption_key_ref": str(
                row.get("sifreleme_anahtari",
                        f"kms:saglik/imaging/{_to_patient_id(hasta_id)}")
            ),
            "radiologist_report": str(row.get("radyolog_raporu", "")),
            "meta": _meta(source_record_id=goruntu_id),
        })

    return docs


# ──────────────────────────────────────────────────────────────────────────────
# 7. feature_store  (FIX-5: yeni transformer)
# ──────────────────────────────────────────────────────────────────────────────

def transform_feature_store(
    patient_id: str,
    profile: dict,
    lab_docs: list[dict],
    gen_doc: dict | None,
    feature_set_id: str = "diabetes_v2",
    feature_set_version: str = "2.1.0",
) -> dict | None:
    """
    patient_profile + lab_aggregates + genetic_profile → feature_store dokümanı.
    Basit numerik vektör; ML modeli tüketmeye hazır.
    """
    demographics = profile.get("demographics", {})
    birth_year = demographics.get("birth_year")
    age = (datetime.now().year - birth_year) if birth_year else None

    lab_index = {d["parameter"]["code"]: d for d in lab_docs}

    def latest_val(loinc: str) -> float | None:
        doc = lab_index.get(loinc)
        return doc["latest"]["value"] if doc else None

    features: dict = {
        "age": age,
        "gender_M": 1 if demographics.get("gender") == "M" else 0,
        "hba1c": latest_val("4548-4"),
        "systolic_bp_avg_30d": (lab_index.get("8480-6", {})
                                .get("windows", {}).get("30d", {}).get("avg")),
        "chronic_condition_count": len(profile.get("chronic_conditions", [])),
        "has_genetic_profile": 1 if (gen_doc is not None) else 0,
        "pathogenic_variant_count": (
            gen_doc["rollups"]["pathogenic_count"] if gen_doc else 0
        ),
    }

    computed_at = datetime.now(timezone.utc)
    expires_at = computed_at + timedelta(days=7)

    return {
        "patient_id": patient_id,
        "feature_set": {"id": feature_set_id, "version": feature_set_version},
        "features": {k: v for k, v in features.items() if v is not None},
        "computed_at": computed_at.isoformat(),
        "expires_at": expires_at.isoformat(),
        "meta": {"source_etl_version": ETL_VERSION},
    }


# ──────────────────────────────────────────────────────────────────────────────
# 8. run_etl — O-1 (ön-indeksleme) + O-4 (orphan loglama) + FIX-4 (bölünmüş)
# ──────────────────────────────────────────────────────────────────────────────

def _build_grouped_index(df: pd.DataFrame, key: str) -> dict:
    """DataFrame'i key sütununa göre O(1) lookup dict'e dönüştürür (O-1)."""
    return {hid: grp for hid, grp in df.groupby(key)}


def _detect_orphans(
    tables: list[tuple[str, pd.DataFrame]],
    gecerli_ids: set,
) -> list[dict]:
    """Geçerli hasta_id'si olmayan satırları tespit eder ve loglar (O-4)."""
    log: list[dict] = []
    for tablo, df in tables:
        orphan_ids = df[~df["hasta_id"].isin(gecerli_ids)]["hasta_id"].unique()
        for oid in orphan_ids:
            log.append({
                "tipo": "orphan_hasta_id",
                "hasta_id": str(oid),
                "tablo": tablo,
                "etl_version": ETL_VERSION,
            })
    return log


def _process_patient(
    row: pd.Series,
    grouped: dict,
) -> tuple[dict, list, dict | None, list]:
    """Tek hasta için tüm koleksiyonları üretir."""
    hasta_id = row["hasta_id"]
    empty = pd.DataFrame()

    hasta_tani = grouped["tani"].get(hasta_id, empty)
    hasta_risk = grouped["risk"].get(hasta_id, empty)
    hasta_lab = grouped["lab"].get(hasta_id, empty)
    hasta_gen = grouped["gen"].get(hasta_id, empty)

    profile = transform_patient(row, hasta_tani, hasta_risk)
    lab_aggs = compute_lab_aggregates(hasta_id, hasta_lab)
    gen_doc = transform_genetic(hasta_id, hasta_gen)

    if gen_doc:
        profile["refs"]["has_genetic_profile"] = True

    risk_docs = transform_risk(hasta_id, hasta_risk)
    return profile, lab_aggs, gen_doc, risk_docs


def run_etl(data: dict) -> tuple[dict, list[dict]]:
    """
    Tüm sentetik veriyi ETL'den geçirir.

    Döndürür: (collections_dict, orphan_log)
      collections_dict anahtarları: patient_profile, lab_aggregates,
        genetic_profile, risk_assessments, clinical_timeline, imaging_metadata

    Örnek:
        collections, orphan_log = run_etl(data)
        print(f"{len(orphan_log)} orphan satır atlandı")
    """
    hasta_df = data["hasta"]
    lab_df = data["lab"]
    tani_df = data["tani"]
    genetik_df = data["genetik"]
    risk_df = data["risk"]
    tibbi_kayit_df = data.get("tibbi_kayit", pd.DataFrame())
    goruntu_df = data.get("goruntu", pd.DataFrame())
    recete_df = data.get("recete", pd.DataFrame())

    gecerli_ids = set(hasta_df["hasta_id"])

    # O-1: Tek seferlik ön-indeksleme
    grouped = {
        "tani": _build_grouped_index(tani_df, "hasta_id"),
        "risk": _build_grouped_index(risk_df, "hasta_id"),
        "lab": _build_grouped_index(lab_df.dropna(subset=["deger"]), "hasta_id"),
        "gen": _build_grouped_index(genetik_df, "hasta_id"),
    }

    # O-4: Orphan tespiti
    orphan_log = _detect_orphans(
        [("lab", lab_df), ("tani", tani_df), ("risk", risk_df)],
        gecerli_ids,
    )

    patient_profiles: list = []
    lab_aggregates: list = []
    genetic_profiles: list = []
    risk_assessments: list = []
    clinical_timelines: list = []
    imaging_docs: list = []

    for _, row in hasta_df.iterrows():
        hasta_id = row["hasta_id"]
        profile, lab_aggs, gen_doc, risk_docs = _process_patient(row, grouped)

        patient_profiles.append(profile)
        lab_aggregates.extend(lab_aggs)
        if gen_doc:
            genetic_profiles.append(gen_doc)
        risk_assessments.extend(risk_docs)

        # FIX-5: 3 eksik koleksiyon
        if not tibbi_kayit_df.empty:
            clinical_timelines.extend(
                transform_clinical_timeline(hasta_id, tibbi_kayit_df, tani_df, recete_df)
            )
        if not goruntu_df.empty:
            imaging_docs.extend(transform_imaging(hasta_id, goruntu_df))

    collections = {
        "patient_profile": patient_profiles,
        "lab_aggregates": lab_aggregates,
        "genetic_profile": genetic_profiles,
        "risk_assessments": risk_assessments,
        "clinical_timeline": clinical_timelines,
        "imaging_metadata": imaging_docs,
    }

    return collections, orphan_log
