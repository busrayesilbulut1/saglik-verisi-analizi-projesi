"""
test_sema.py — Katman A: Alan / Tip / KVKK Testleri (10 test)

ETL çıktısındaki dokümanların şema uyumunu doğrular:
- Zorunlu alanlar mevcut mu?
- Tipler ve enum değerleri doğru mu?
- PII alanları MongoDB dokümanına sızmadı mı?
"""

import re

from etl_donusturucu import (
    ICD10_PATTERN,
    PATIENT_ID_PATTERN,
    PII_FIELDS,
    VALID_BLOOD_TYPES,
    VALID_CLINICAL_SIGNIFICANCE,
    VALID_GENDERS,
    VALID_RISK_LEVELS,
    run_etl,
)
from sentetik_veri import make_all


def run(results: list[dict]) -> list[dict]:
    data = make_all(n_hasta=100)
    etl_out = run_etl(data)

    profiles = etl_out["patient_profile"]
    labs = etl_out["lab_aggregates"]
    genetics = etl_out["genetic_profile"]
    risks = etl_out["risk_assessments"]

    # ── TEST A-01: patient_id format ──────────────────────────────────────────
    try:
        invalid = [p["patient_id"] for p in profiles if not PATIENT_ID_PATTERN.match(p["patient_id"])]
        assert len(invalid) == 0, f"Hatalı patient_id: {invalid[:3]}"
        results.append({"test": "patient_id Format", "sonuc": "✅", "detay": f"{len(profiles)} profil kontrol edildi"})
    except AssertionError as e:
        results.append({"test": "patient_id Format", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-02: PII alan yasağı ────────────────────────────────────────────
    try:
        def check_pii(doc: dict, path: str = "") -> list[str]:
            found = []
            for key, val in doc.items():
                full = f"{path}.{key}" if path else key
                if key in PII_FIELDS:
                    found.append(full)
                if isinstance(val, dict):
                    found.extend(check_pii(val, full))
            return found

        pii_leaks = []
        for p in profiles:
            pii_leaks.extend(check_pii(p))

        assert len(pii_leaks) == 0, f"PII sızıntısı: {pii_leaks[:5]}"
        results.append({"test": "PII Alan Yasağı (tc_kimlik_no, ad, soyad, email, telefon)", "sonuc": "✅", "detay": "Hiçbir PII alanı bulunamadı"})
    except AssertionError as e:
        results.append({"test": "PII Alan Yasağı", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-03: birth_year tipi ve aralığı ─────────────────────────────────
    try:
        invalid_years = []
        for p in profiles:
            by = p.get("demographics", {}).get("birth_year")
            if by is not None:
                assert isinstance(by, int), f"int değil: {type(by)}"
                assert 1900 <= by <= 2026, f"Aralık dışı: {by}"
        results.append({"test": "birth_year Tipi ve Aralığı", "sonuc": "✅", "detay": "int, 1900-2026"})
    except AssertionError as e:
        results.append({"test": "birth_year Tipi ve Aralığı", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-04: gender enum ───────────────────────────────────────────────
    try:
        valid_g = {"M", "F", "OTHER"}
        invalid_g = [p["demographics"]["gender"] for p in profiles if p["demographics"]["gender"] not in valid_g]
        assert len(invalid_g) == 0, f"Geçersiz cinsiyet: {set(invalid_g)}"
        results.append({"test": "Gender Enum (M/F/OTHER)", "sonuc": "✅", "detay": "Tüm değerler geçerli"}) # OTHER --> Belirtmek istemeyen
    except AssertionError as e:
        results.append({"test": "Gender Enum", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-05: blood_type enum ───────────────────────────────────────────
    try:
        invalid_bt = [
            p["demographics"].get("blood_type")
            for p in profiles
            if p["demographics"].get("blood_type") is not None
            and p["demographics"]["blood_type"] not in VALID_BLOOD_TYPES
        ]
        assert len(invalid_bt) == 0, f"Geçersiz kan grubu: {set(invalid_bt)}"
        results.append({"test": "blood_type Enum", "sonuc": "✅", "detay": "Tüm değerler geçerli"})
    except AssertionError as e:
        results.append({"test": "blood_type Enum", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-06: ICD-10 format ─────────────────────────────────────────────
    try:
        invalid_icd = []
        for p in profiles:
            for cond in p.get("chronic_conditions", []):
                icd = cond.get("icd10", "")
                if not ICD10_PATTERN.match(icd):
                    invalid_icd.append(icd)
        assert len(invalid_icd) == 0, f"Hatalı ICD-10: {invalid_icd[:5]}"
        results.append({"test": "ICD-10 Format (^[A-Z][0-9]{{2}})", "sonuc": "✅", "detay": "Lowercase kodlar filtrelendi"})
    except AssertionError as e:
        results.append({"test": "ICD-10 Format", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-07: risk_score aralığı ─────────────────────────────────────────
    try:
        invalid_rs = [
            r["risk_score"] for r in risks
            if not (0.0 <= r["risk_score"] <= 1.0)
        ]
        assert len(invalid_rs) == 0, f"Aralık dışı risk_score: {invalid_rs[:5]}"
        results.append({"test": "risk_score Aralığı (0.0–1.0)", "sonuc": "✅", "detay": f"{len(risks)} değerlendirme kontrol edildi"})
    except AssertionError as e:
        results.append({"test": "risk_score Aralığı", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-08: risk_level enum ───────────────────────────────────────────
    try:
        invalid_rl = [r["risk_level"] for r in risks if r["risk_level"] not in VALID_RISK_LEVELS]
        assert len(invalid_rl) == 0, f"Geçersiz risk_level: {set(invalid_rl)}"
        results.append({"test": "risk_level Enum (LOW/MEDIUM/HIGH/CRITICAL)", "sonuc": "✅", "detay": "Tüm değerler geçerli"})
    except AssertionError as e:
        results.append({"test": "risk_level Enum", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-09: clinical_significance enum ─────────────────────────────────
    try:
        invalid_cs = [
            v["clinical_significance"]
            for g in genetics
            for v in g.get("variants", [])
            if v["clinical_significance"] not in VALID_CLINICAL_SIGNIFICANCE
        ]
        assert len(invalid_cs) == 0, f"Geçersiz clinical_significance: {set(invalid_cs)}"
        results.append({"test": "clinical_significance Enum", "sonuc": "✅", "detay": "Tüm varyantlar geçerli"})
    except AssertionError as e:
        results.append({"test": "clinical_significance Enum", "sonuc": "❌", "detay": str(e)})

    # ── TEST A-10: meta.last_synced varlığı ──────────────────────────────────
    try:
        all_docs = profiles + labs + genetics + risks
        missing_meta = [
            i for i, doc in enumerate(all_docs)
            if not doc.get("meta", {}).get("last_synced")
        ]
        assert len(missing_meta) == 0, f"{len(missing_meta)} dokümanda meta.last_synced eksik"
        results.append({"test": "meta.last_synced Varlığı", "sonuc": "✅", "detay": f"{len(all_docs)} doküman kontrol edildi"})
    except AssertionError as e:
        results.append({"test": "meta.last_synced Varlığı", "sonuc": "❌", "detay": str(e)})

    return results
