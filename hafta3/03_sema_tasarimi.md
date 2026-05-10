# 03 — Şema Tasarımı: 7 Koleksiyon

## Genel Yaklaşım

- **Veritabanı adı:** `saglik_analitik`
- **Doküman ID kuralı:** her koleksiyonda business key (`patient_id`, `assessment_id` vb.) kullanılır; MongoDB'nin `_id` alanı otomatik `ObjectId` üretir.
- **Tarih alanları:** ISO 8601 / UTC (`ISODate("2026-05-07T03:00:00Z")`).
- **patient_id formatı:** `pt_[a-z0-9]{8}` — Melek'in API'siyle birebir uyumlu.

### Embed mi, Reference mı? — Hızlı kılavuz

| Durum | Karar |
|---|---|
| Veri küçük (< 100 alt eleman) ve birlikte okunuyor | **Embed** |
| Veri büyür ve ayrı sorgulanıyor | **Reference** (ayrı koleksiyon, `patient_id` ile bağla) |
| Veri çok büyük (binary, GB) | **External** (HDFS) + path referansı |
| Pre-aggregated (rollup) | **Embed** (denormalize, performans için) |

---

## 1. `patient_profile`

**Amaç:** Hasta hakkında tek bakışta her şey. Dashboard'un ilk yüklediği koleksiyon.

**Embed kararı:** demografi, kronik durumlar, alerjiler, rollup'lar embed edilir (küçük + birlikte okunur). Lab kayıtları, genetik varyantlar, görüntüler ayrı koleksiyonlarda kalır (büyür).

```javascript
{
  _id: ObjectId("..."),
  patient_id: "pt_7f3a9b2c",
  demographics: {
    birth_year: 1985,
    gender: "M",                  // M | F | OTHER
    blood_type: "A+",             // A+/A-/B+/B-/AB+/AB-/0+/0-
    city: "Istanbul"              // Şehir bazlı kohort analizi için
  },
  chronic_conditions: [
    {
      icd10: "E11",
      name: "Type 2 Diabetes",
      diagnosed_at: ISODate("2020-03-15T00:00:00Z"),
      severity: "MEDIUM"          // LOW | MEDIUM | HIGH
    },
    {
      icd10: "I10",
      name: "Essential Hypertension",
      diagnosed_at: ISODate("2022-01-10T00:00:00Z"),
      severity: "MEDIUM"
    }
  ],
  allergies: ["PENICILLIN", "ASPIRIN"],
  rollups: {
    last_hba1c: 7.2,
    last_hba1c_at: ISODate("2026-04-20T08:30:00Z"),
    avg_systolic_30d: 138.4,
    avg_diastolic_30d: 86.2,
    bmi_latest: 28.4,
    risk_scores: {
      diabetes: 0.74,
      cardiovascular: 0.51,
      cancer_breast: 0.12
    },
    last_updated: ISODate("2026-05-07T03:00:00Z")
  },
  refs: {
    has_genetic_profile: true,
    imaging_count: 3,
    latest_assessment_id: "ras_00123",
    timeline_event_count: 47
  },
  meta: {
    source_db: "postgres_main",
    etl_version: "v1.2",
    last_synced: ISODate("2026-05-07T03:00:00Z")
  }
}
```

**Tipik sorgu:** `db.patient_profile.findOne({ patient_id: "pt_7f3a9b2c" })`

---

## 2. `clinical_timeline`

**Amaç:** Hastanın tüm klinik olaylarını kronolojik sırayla. Doktor zaman çizelgesi ekranını besler.

**Embed kararı:** her satır bir olay; tanılar ve reçete özeti embed edilir.

```javascript
{
  _id: ObjectId("..."),
  patient_id: "pt_7f3a9b2c",
  event_id: "evt_a1b2c3d4",
  event_type: "POLIKLINIK",       // POLIKLINIK | YATIS | ACIL | LAB | IMAGING | GENETIC
  event_at: ISODate("2026-04-20T08:30:00Z"),
  doctor_id_hash: "sha256:abc123...",
  facility: "Istanbul Tip Fakultesi Hastanesi",
  complaint: "Kontrol muayenesi, baş ağrısı şikayeti",
  diagnoses: [
    { icd10: "E11.9", name: "Type 2 Diabetes (uncomplicated)" }
  ],
  prescriptions_summary: {
    prescription_count: 1,
    medication_count: 2,
    medications: ["Metformin 1000mg", "Atorvastatin 20mg"]
  },
  notes_excerpt: "Glisemi kontrolü iyileşiyor. Diyet uyumu artırılmalı.",
  meta: {
    source_record_id: "kayit_uuid_postgres",
    last_synced: ISODate("2026-05-07T03:00:00Z")
  }
}
```

**Tipik sorgu:** `db.clinical_timeline.find({ patient_id: "pt_7f3a9b2c" }).sort({ event_at: -1 }).limit(50)`

---

## 3. `lab_aggregates`

**Amaç:** Her hasta-parametre çifti için pre-aggregated lab metrikleri. Trend grafikleri saniyenin altında render eder.

**Embed kararı:** windows (30g/90g/1y) embed; tek tek ölçüm değerleri ayrı `lab_results` koleksiyonunda tutulabilir (bu görev kapsamı dışı, gerekirse Hafta 5).

```javascript
{
  _id: ObjectId("..."),
  patient_id: "pt_7f3a9b2c",
  parameter: {
    code: "4548-4",               // LOINC
    name: "HbA1c",
    unit: "%",
    reference_range: { min: 4.0, max: 5.6 }
  },
  windows: {
    "7d":  { min: 7.0, max: 7.4, avg: 7.2, count: 1 },
    "30d": { min: 6.9, max: 7.4, avg: 7.15, count: 2 },
    "90d": { min: 6.8, max: 7.4, avg: 7.10, count: 4 },
    "1y":  { min: 6.5, max: 7.6, avg: 7.05, count: 8 }
  },
  latest: {
    value: 7.2,
    measured_at: ISODate("2026-04-20T08:30:00Z"),
    is_abnormal: true,
    abnormal_direction: "HIGH"    // HIGH | LOW | null
  },
  trend: {
    direction: "INCREASING",      // INCREASING | DECREASING | STABLE
    slope_per_month: 0.05,
    last_updated: ISODate("2026-05-07T03:00:00Z")
  },
  meta: {
    last_synced: ISODate("2026-05-07T03:00:00Z")
  }
}
```

**Tipik sorgu:** `db.lab_aggregates.find({ patient_id: "pt_7f3a9b2c", "parameter.code": "4548-4" })`

---

## 4. `genetic_profile`

**Amaç:** Hastanın genetik analiz özetini ve klinik öneme sahip varyantlarını tutar.

**Embed kararı:** Klinik öneme sahip varyantlar embed edilir (tipik 100-1.000 varyant). **Tüm WGS varyantları (~3 milyon) embed edilmez** — ham VCF dosyası HDFS'te kalır, sadece path tutulur.

```javascript
{
  _id: ObjectId("..."),
  patient_id: "pt_7f3a9b2c",
  analysis_type: "WES",           // WGS | WES | SNP_PANEL | PHARMACOGENOMICS
  platform: "Illumina NovaSeq",
  analyzed_at: ISODate("2025-08-15T00:00:00Z"),
  variants: [
    {
      gene: "BRCA1",
      rsid: "rs80357906",
      position: "chr17:43093454",
      allele: "C>T",
      clinical_significance: "PATHOGENIC",
      risk_score: 0.85,
      conditions: ["Breast cancer", "Ovarian cancer"]
    },
    {
      gene: "TCF7L2",
      rsid: "rs7903146",
      position: "chr10:114758349",
      allele: "C>T",
      clinical_significance: "RISK_FACTOR",
      risk_score: 0.40,
      conditions: ["Type 2 Diabetes"]
    }
  ],
  rollups: {
    total_variants_called: 4_200_000,    // Ham dosyadaki toplam
    clinically_significant_count: 23,
    pathogenic_count: 2,
    likely_pathogenic_count: 5,
    vus_count: 16
  },
  raw_file: {
    hdfs_path: "/data/genetic/pt_7f3a9b2c/wes_2025_08_15.vcf.gz",
    encryption_key_ref: "kms:saglik/genetic/pt_7f3a9b2c",
    file_size_bytes: 248_000_000
  },
  meta: {
    last_synced: ISODate("2026-05-07T03:00:00Z")
  }
}
```

**Tipik sorgu:** `db.genetic_profile.find({ "variants.gene": "BRCA1", "variants.clinical_significance": "PATHOGENIC" })`

---

## 5. `imaging_metadata`

**Amaç:** DICOM görüntü metadata'sı. Ham görüntü HDFS'te şifreli; bu koleksiyon sadece arama, filtreleme ve radyolog raporunu tutar.

**Embed kararı:** Yok — her görüntü ayrı doküman, hasta başına çok sayıda görüntü olabilir.

```javascript
{
  _id: ObjectId("..."),
  patient_id: "pt_7f3a9b2c",
  dicom_uid: "1.2.840.113619.2.55.3.4271891.123.1614602400.1234",
  modality: "MRI",                // MRI | CT | X-RAY | ULTRASOUND | PET
  body_part: "BRAIN",
  captured_at: ISODate("2026-03-10T14:30:00Z"),
  facility: "Istanbul Tip Fakultesi Radyoloji",
  hdfs_path: "/data/imaging/pt_7f3a9b2c/mri_brain_20260310.dcm",
  file_size_bytes: 142_000_000,
  encryption_key_ref: "kms:saglik/imaging/pt_7f3a9b2c",
  radiologist_report: "Sağ frontal lobda 8mm hiperintens lezyon görülmüş...",
  ai_analysis: {
    model_version: "monai_brain_v1.3",
    findings: ["lesion_frontal_right"],
    confidence: 0.87,
    processed_at: ISODate("2026-03-10T15:00:00Z")
  },
  meta: {
    source_record_id: "goruntu_uuid_postgres",
    last_synced: ISODate("2026-05-07T03:00:00Z")
  }
}
```

**Tipik sorgu:** Tam metin arama radyolog raporunda.
```javascript
db.imaging_metadata.find({
  patient_id: "pt_7f3a9b2c",
  modality: "MRI",
  $text: { $search: "lezyon hiperintens" }
})
```

---

## 6. `risk_assessments`

**Amaç:** Model çıktıları. Her risk hesabı yeni bir doküman; geçmiş tutulur (model versiyon farkını analiz için).

**Embed kararı:** öneriler küçük + birlikte okunur → embed. Contributing factors model çıktısı → embed.

```javascript
{
  _id: ObjectId("..."),
  assessment_id: "ras_00123",
  patient_id: "pt_7f3a9b2c",
  disease: "Type 2 Diabetes",
  risk_score: 0.74,
  risk_level: "HIGH",             // LOW (0-0.3) | MEDIUM (0.3-0.6) | HIGH (0.6-0.8) | CRITICAL (0.8-1.0)
  confidence: 0.89,
  prediction_horizon_months: 12,
  model: {
    id: "mdl_diabetes_v2",
    version: "2.1.0",
    algorithm: "Random Forest",
    trained_at: ISODate("2026-02-15T00:00:00Z")
  },
  contributing_factors: [
    { factor: "HbA1c", importance: 0.42, direction: "POSITIVE", value: 7.2 },
    { factor: "BMI", importance: 0.28, direction: "POSITIVE", value: 28.4 },
    { factor: "physical_activity", importance: 0.15, direction: "NEGATIVE", value: "low" },
    { factor: "TCF7L2_variant", importance: 0.10, direction: "POSITIVE", value: "C/T" }
  ],
  recommendations: [
    {
      type: "LIFESTYLE",
      priority: "HIGH",
      title: "Fiziksel Aktivite Artışı",
      description: "Haftada en az 150 dakika orta yoğunlukta aerobik egzersiz",
      evidence_level: "A"
    },
    {
      type: "SCREENING",
      priority: "HIGH",
      title: "3 Aylık HbA1c Takibi",
      description: "Kan şekeri kontrolü için 3 ayda bir HbA1c testi",
      evidence_level: "A"
    }
  ],
  computed_at: ISODate("2026-05-07T03:15:00Z"),
  valid_until: ISODate("2026-06-07T03:15:00Z"),
  meta: {
    triggered_by: "scheduled_batch",   // scheduled_batch | api_request | data_change
    last_synced: ISODate("2026-05-07T03:15:00Z")
  }
}
```

**Tipik sorgu:** `db.risk_assessments.find({ patient_id: "pt_7f3a9b2c", disease: "Type 2 Diabetes" }).sort({ computed_at: -1 }).limit(10)`

---

## 7. `feature_store`

**Amaç:** ML modellerinin tüketmeye hazır feature vektörleri. Her hasta-model kombinasyonu için tek doküman, günde bir kez recompute edilir.

**Embed kararı:** features tek bir object, küçük (~50 feature). TTL ile eski versiyonlar otomatik silinir.

```javascript
{
  _id: ObjectId("..."),
  patient_id: "pt_7f3a9b2c",
  feature_set: {
    id: "diabetes_v2",
    version: "2.1.0"
  },
  features: {
    age: 41,
    gender_M: 1,
    bmi: 28.4,
    hba1c: 7.2,
    fasting_glucose: 142,
    systolic_bp_avg_30d: 138.4,
    diastolic_bp_avg_30d: 86.2,
    has_pathogenic_brca1: 0,
    has_risk_tcf7l2: 1,
    physical_activity_score: 2,
    smoking_status_current: 0,
    family_history_diabetes: 1,
    chronic_condition_count: 2
  },
  computed_at: ISODate("2026-05-07T03:00:00Z"),
  expires_at: ISODate("2026-05-14T03:00:00Z"),  // TTL → 7 gün
  meta: {
    source_etl_version: "v1.2",
    feature_drift_score: 0.04          // Önceki recompute'a göre değişim
  }
}
```

**Tipik sorgu:** `db.feature_store.findOne({ patient_id: "pt_7f3a9b2c", "feature_set.id": "diabetes_v2" })`

---

## Özet Tablosu

| Koleksiyon | Doküman/hasta | Tahmini boyut/doküman | Birincil sorgu |
|---|---|---|---|
| `patient_profile` | 1 | ~5 KB | `findOne(patient_id)` |
| `clinical_timeline` | 50-500 | ~1 KB | `find(patient_id).sort(event_at).limit()` |
| `lab_aggregates` | 20-100 (parametre başına) | ~2 KB | `find(patient_id, parameter.code)` |
| `genetic_profile` | 0-1 | ~50 KB (klinik varyantlar) | `findOne(patient_id)` |
| `imaging_metadata` | 0-50 | ~10 KB (rapor metni) | `find(patient_id, modality)` |
| `risk_assessments` | 5-100 (zamanla) | ~3 KB | `find(patient_id, disease).sort(computed_at)` |
| `feature_store` | 1-5 (model başına) | ~1 KB | `findOne(patient_id, feature_set.id)` |

## Tasarım Kararları — Akın'ın Şemasıyla Karşılaştırma

| Konu | Akın (PostgreSQL) | Sezer (MongoDB) | Gerekçe |
|---|---|---|---|
| Hasta-tanı ilişkisi | Ayrı `tani` tablosu, FK | Aktif kronikler `patient_profile` içinde embed | Read latency'yi 2 sorgu → 1 sorguya indirir |
| Lab sonucu | Her ölçüm `lab_sonuc` satırı | Pre-aggregated rollup'lar | Trend grafiği render hızı |
| Genetik varyant | Her varyant ayrı satır | Klinik önemli olanlar embed array | Tipik sorgu hep tüm önemli varyantları çeker |
| Audit log | `denetim_kaydi` (her değişiklik) | YOK | Audit OLTP'de kalır; analitik depo log tutmaz |
| FK kısıtı | Veritabanı seviyesinde | YOK (uygulama katmanında) | NoSQL felsefesi; ETL job'u izlenebilirliği sağlar |
