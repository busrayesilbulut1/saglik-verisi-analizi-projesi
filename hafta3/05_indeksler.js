// ============================================================================
// Sağlık Analitik MongoDB — İndeks Tanımları
// Hedef: MongoDB 7.0+
//
// Strateji: sorgu kalıbı → indeks. Her aggregation pipeline'ın $match aşaması
// bir indeks tarafından desteklenmelidir. Bkz. 07_sorgu_ornekleri.js
// ============================================================================

use("saglik_analitik");

// ----------------------------------------------------------------------------
// 1. patient_profile
// ----------------------------------------------------------------------------
// Tek doküman lookup
db.patient_profile.createIndex(
  { patient_id: 1 },
  { unique: true, name: "ux_patient_id" }
);

// Kohort: cinsiyet × yaş aralığı
db.patient_profile.createIndex(
  { "demographics.gender": 1, "demographics.birth_year": 1 },
  { name: "ix_gender_birth_year" }
);

// Şehir bazlı kohort
db.patient_profile.createIndex(
  { "demographics.city": 1 },
  { name: "ix_city" }
);

// Kronik durum filtresi (ICD-10 koduna göre)
db.patient_profile.createIndex(
  { "chronic_conditions.icd10": 1 },
  { name: "ix_chronic_icd10" }
);

// Yüksek riskli hastalar — diabetes
db.patient_profile.createIndex(
  { "rollups.risk_scores.diabetes": -1 },
  { name: "ix_risk_diabetes_desc", sparse: true }
);

// Yüksek riskli hastalar — cardiovascular
db.patient_profile.createIndex(
  { "rollups.risk_scores.cardiovascular": -1 },
  { name: "ix_risk_cv_desc", sparse: true }
);

// ETL job'u: son senkronize tarihten sonra değişenler
db.patient_profile.createIndex(
  { "meta.last_synced": 1 },
  { name: "ix_last_synced" }
);

// ----------------------------------------------------------------------------
// 2. clinical_timeline
// ----------------------------------------------------------------------------
// Hasta zaman çizelgesi: birincil sorgu
db.clinical_timeline.createIndex(
  { patient_id: 1, event_at: -1 },
  { name: "ix_patient_event_desc" }
);

// Olay tipi filtresi (yatış, acil vb.)
db.clinical_timeline.createIndex(
  { patient_id: 1, event_type: 1, event_at: -1 },
  { name: "ix_patient_type_event" }
);

// Tanı bazlı kohort (tüm hastalarda belirli ICD-10)
db.clinical_timeline.createIndex(
  { "diagnoses.icd10": 1, event_at: -1 },
  { name: "ix_diagnosis_icd10" }
);

// Doktor pseudonim üzerinden iş yükü analizi
db.clinical_timeline.createIndex(
  { doctor_id_hash: 1, event_at: -1 },
  { name: "ix_doctor_hash_event", sparse: true }
);

// ----------------------------------------------------------------------------
// 3. lab_aggregates
// ----------------------------------------------------------------------------
// Hasta + parametre — tek doküman lookup
db.lab_aggregates.createIndex(
  { patient_id: 1, "parameter.code": 1 },
  { unique: true, name: "ux_patient_param" }
);

// Anormal lab sonuçları — alerting için
db.lab_aggregates.createIndex(
  { patient_id: 1, "latest.is_abnormal": 1 },
  { name: "ix_patient_abnormal" }
);

// Parametre bazlı kohort: "HbA1c yüksek olan tüm hastalar"
db.lab_aggregates.createIndex(
  { "parameter.code": 1, "latest.value": 1 },
  { name: "ix_param_value" }
);

// Trend yönü filtresi
db.lab_aggregates.createIndex(
  { "parameter.code": 1, "trend.direction": 1 },
  { name: "ix_param_trend" }
);

// ----------------------------------------------------------------------------
// 4. genetic_profile
// ----------------------------------------------------------------------------
// Hasta bazlı lookup
db.genetic_profile.createIndex(
  { patient_id: 1 },
  { unique: true, name: "ux_patient_id" }
);

// Belirli gen + klinik öneme sahip varyant kohortu
db.genetic_profile.createIndex(
  { "variants.gene": 1, "variants.clinical_significance": 1 },
  { name: "ix_gene_significance" }
);

// rsid bazlı arama (ClinVar entegrasyonu için)
db.genetic_profile.createIndex(
  { "variants.rsid": 1 },
  { name: "ix_rsid", sparse: true }
);

// Patojenik varyantı olan hastalar
db.genetic_profile.createIndex(
  { "rollups.pathogenic_count": -1 },
  { name: "ix_pathogenic_count_desc" }
);

// ----------------------------------------------------------------------------
// 5. imaging_metadata
// ----------------------------------------------------------------------------
// DICOM UID — global unique
db.imaging_metadata.createIndex(
  { dicom_uid: 1 },
  { unique: true, name: "ux_dicom_uid" }
);

// Hasta + modalite (MR, CT vb.)
db.imaging_metadata.createIndex(
  { patient_id: 1, modality: 1, captured_at: -1 },
  { name: "ix_patient_modality_captured" }
);

// Vücut bölgesi bazlı kohort
db.imaging_metadata.createIndex(
  { modality: 1, body_part: 1 },
  { name: "ix_modality_body_part" }
);

// AI analiz bulguları
db.imaging_metadata.createIndex(
  { "ai_analysis.findings": 1 },
  { name: "ix_ai_findings", sparse: true }
);

// Radyolog raporu üzerinde tam metin araması
db.imaging_metadata.createIndex(
  { radiologist_report: "text" },
  {
    name: "tx_radiologist_report",
    default_language: "turkish",
    weights: { radiologist_report: 10 }
  }
);

// ----------------------------------------------------------------------------
// 6. risk_assessments
// ----------------------------------------------------------------------------
// Hasta + hastalık + zaman: en son skoru getir
db.risk_assessments.createIndex(
  { patient_id: 1, disease: 1, computed_at: -1 },
  { name: "ix_patient_disease_computed" }
);

// assessment_id — API endpoint'i tarafından kullanılıyor
db.risk_assessments.createIndex(
  { assessment_id: 1 },
  { unique: true, name: "ux_assessment_id" }
);

// Yüksek riskli hastaları tarama (kritik hastalık alarmı)
db.risk_assessments.createIndex(
  { disease: 1, risk_level: 1, computed_at: -1 },
  { name: "ix_disease_level_computed" }
);

// Model versiyonu bazlı analiz
db.risk_assessments.createIndex(
  { "model.id": 1, "model.version": 1, computed_at: -1 },
  { name: "ix_model_version_computed" }
);

// ----------------------------------------------------------------------------
// 7. feature_store
// ----------------------------------------------------------------------------
// Hasta + feature set lookup
db.feature_store.createIndex(
  { patient_id: 1, "feature_set.id": 1, "feature_set.version": 1 },
  { unique: true, name: "ux_patient_featureset_version" }
);

// TTL — 7 günden eski feature vektörleri otomatik silinir
db.feature_store.createIndex(
  { expires_at: 1 },
  { name: "ttl_expires_at", expireAfterSeconds: 0 }
);

// Drift skoru analizi (model bozulma takibi)
db.feature_store.createIndex(
  { "feature_set.id": 1, "meta.feature_drift_score": -1 },
  { name: "ix_featureset_drift", sparse: true }
);

// ----------------------------------------------------------------------------
// Doğrulama
// ----------------------------------------------------------------------------
const collections = [
  "patient_profile",
  "clinical_timeline",
  "lab_aggregates",
  "genetic_profile",
  "imaging_metadata",
  "risk_assessments",
  "feature_store"
];

print("\n=== İndeks Kurulum Özeti ===");
collections.forEach(name => {
  const indexes = db[name].getIndexes();
  print(`\n${name} (${indexes.length} indeks):`);
  indexes.forEach(idx => print(`  - ${idx.name}: ${JSON.stringify(idx.key)}`));
});
