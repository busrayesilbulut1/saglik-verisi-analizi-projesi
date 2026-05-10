// ============================================================================
// Sağlık Analitik MongoDB — Aggregation Pipeline Örnekleri
//
// Her sorgu Melek'in API'sindeki bir endpoint veya istatistiksel analiz
// modülünün bir use case'ini karşılar. Tüm $match aşamaları 05_indeksler.js
// içindeki bir indeks tarafından desteklenir.
//
// Kullanım: mongosh < 07_sorgu_ornekleri.js
// ============================================================================

use("saglik_analitik");

// ----------------------------------------------------------------------------
// 1. Yüksek Riskli Diyabet Hastaları (HIGH veya CRITICAL)
//
// API: GET /reports/visualizations?chart_type=RISK_GAUGE
// İndeks: ix_disease_level_computed
// ----------------------------------------------------------------------------
print("\n--- 1. Yüksek riskli diyabet hastaları ---");
db.risk_assessments.aggregate([
  {
    $match: {
      disease: "Type 2 Diabetes",
      risk_level: { $in: ["HIGH", "CRITICAL"] },
      computed_at: { $gte: ISODate("2026-04-01T00:00:00Z") }
    }
  },
  {
    $sort: { computed_at: -1 }
  },
  // Her hasta için sadece en son skoru
  {
    $group: {
      _id: "$patient_id",
      latest_score: { $first: "$risk_score" },
      latest_level: { $first: "$risk_level" },
      computed_at: { $first: "$computed_at" }
    }
  },
  {
    $sort: { latest_score: -1 }
  },
  {
    $limit: 100
  }
]);

// ----------------------------------------------------------------------------
// 2. Belirli Hasta için Son 6 Ayın HbA1c Trendi
//
// API: GET /reports/visualizations/{patient_id}?chart_type=TREND&metric=HbA1c
// İndeks: ux_patient_param
// ----------------------------------------------------------------------------
print("\n--- 2. HbA1c trendi (son 6 ay) ---");
db.lab_aggregates.aggregate([
  {
    $match: {
      patient_id: "pt_7f3a9b2c",
      "parameter.code": "4548-4"
    }
  },
  {
    $project: {
      _id: 0,
      patient_id: 1,
      parameter_name: "$parameter.name",
      unit: "$parameter.unit",
      reference_range: "$parameter.reference_range",
      // Son 6 aylık trend için 90d penceresi yaklaşıkıdır; gerçek
      // sürümde lab_results koleksiyonundaki ham ölçümler kullanılır.
      windows: 1,
      latest: 1,
      trend: 1
    }
  }
]);

// ----------------------------------------------------------------------------
// 3. Belirli Genetik Varyanta Sahip Hasta Kohortu
//
// Use case: ML model eğitimi için BRCA1 patojenik varyantı taşıyan tüm hastalar
// İndeks: ix_gene_significance
// ----------------------------------------------------------------------------
print("\n--- 3. BRCA1 patojenik kohort ---");
db.genetic_profile.aggregate([
  {
    $match: {
      variants: {
        $elemMatch: {
          gene: "BRCA1",
          clinical_significance: "PATHOGENIC"
        }
      }
    }
  },
  {
    $project: {
      _id: 0,
      patient_id: 1,
      analysis_type: 1,
      analyzed_at: 1,
      brca1_variants: {
        $filter: {
          input: "$variants",
          as: "v",
          cond: {
            $and: [
              { $eq: ["$$v.gene", "BRCA1"] },
              { $eq: ["$$v.clinical_significance", "PATHOGENIC"] }
            ]
          }
        }
      }
    }
  }
]);

// ----------------------------------------------------------------------------
// 4. Cinsiyet × Yaş Aralığı × Kronik Durum Cross-Tabulation
//
// API: POST /analysis/statistical { analysis_type: "DESCRIPTIVE" }
// İndeks: ix_gender_birth_year + ix_chronic_icd10
// $facet ile tek geçişte birden fazla agregasyon
// ----------------------------------------------------------------------------
print("\n--- 4. Cross-tab: cinsiyet × yaş × kronik durum ---");
db.patient_profile.aggregate([
  {
    $match: {
      "chronic_conditions.icd10": { $in: ["E11", "I10", "E78.0"] }
    }
  },
  {
    $addFields: {
      age: { $subtract: [2026, "$demographics.birth_year"] },
      age_band: {
        $switch: {
          branches: [
            { case: { $lt: [{ $subtract: [2026, "$demographics.birth_year"] }, 30] }, then: "<30" },
            { case: { $lt: [{ $subtract: [2026, "$demographics.birth_year"] }, 50] }, then: "30-49" },
            { case: { $lt: [{ $subtract: [2026, "$demographics.birth_year"] }, 70] }, then: "50-69" }
          ],
          default: "70+"
        }
      }
    }
  },
  {
    $facet: {
      by_gender: [
        { $group: { _id: "$demographics.gender", count: { $sum: 1 } } }
      ],
      by_age_band: [
        { $group: { _id: "$age_band", count: { $sum: 1 } } },
        { $sort: { _id: 1 } }
      ],
      by_condition: [
        { $unwind: "$chronic_conditions" },
        { $group: { _id: "$chronic_conditions.icd10", count: { $sum: 1 } } },
        { $sort: { count: -1 } }
      ],
      cross_gender_age: [
        {
          $group: {
            _id: { gender: "$demographics.gender", age_band: "$age_band" },
            count: { $sum: 1 }
          }
        },
        { $sort: { "_id.gender": 1, "_id.age_band": 1 } }
      ]
    }
  }
]);

// ----------------------------------------------------------------------------
// 5. Hasta Tam Profili — Dashboard İlk Yükleme
//
// API: GET /patients/{patient_id} + ek veri
// 4 koleksiyondan $lookup ile birleştirir.
// İndeks: ux_patient_id (her koleksiyonda)
// ----------------------------------------------------------------------------
print("\n--- 5. Hasta dashboard payload ---");
db.patient_profile.aggregate([
  { $match: { patient_id: "pt_7f3a9b2c" } },
  {
    $lookup: {
      from: "risk_assessments",
      let: { pid: "$patient_id" },
      pipeline: [
        { $match: { $expr: { $eq: ["$patient_id", "$$pid"] } } },
        { $sort: { computed_at: -1 } },
        { $limit: 5 }
      ],
      as: "recent_assessments"
    }
  },
  {
    $lookup: {
      from: "clinical_timeline",
      let: { pid: "$patient_id" },
      pipeline: [
        { $match: { $expr: { $eq: ["$patient_id", "$$pid"] } } },
        { $sort: { event_at: -1 } },
        { $limit: 10 }
      ],
      as: "recent_events"
    }
  },
  {
    $lookup: {
      from: "lab_aggregates",
      localField: "patient_id",
      foreignField: "patient_id",
      as: "lab_metrics"
    }
  }
]);

// ----------------------------------------------------------------------------
// 6. Anormal Lab Sonucu Olan Hastalar — Alarm Listesi
//
// Use case: oncall doktor için günlük alert listesi
// İndeks: ix_param_value
// ----------------------------------------------------------------------------
print("\n--- 6. HbA1c > 8.0 olan hastalar ---");
db.lab_aggregates.aggregate([
  {
    $match: {
      "parameter.code": "4548-4",
      "latest.value": { $gt: 8.0 },
      "latest.measured_at": { $gte: ISODate("2026-04-01T00:00:00Z") }
    }
  },
  {
    $lookup: {
      from: "patient_profile",
      localField: "patient_id",
      foreignField: "patient_id",
      as: "profile"
    }
  },
  { $unwind: "$profile" },
  {
    $project: {
      _id: 0,
      patient_id: 1,
      hba1c: "$latest.value",
      measured_at: "$latest.measured_at",
      gender: "$profile.demographics.gender",
      birth_year: "$profile.demographics.birth_year",
      diabetes_risk: "$profile.rollups.risk_scores.diabetes"
    }
  },
  { $sort: { hba1c: -1 } }
]);

// ----------------------------------------------------------------------------
// 7. Model Versiyonu Karşılaştırması — A/B Test
//
// Use case: yeni model versiyonu (v2.1.0) eskisinden (v2.0.0) daha iyi mi?
// İndeks: ix_model_version_computed
// ----------------------------------------------------------------------------
print("\n--- 7. Model versiyon karşılaştırması ---");
db.risk_assessments.aggregate([
  {
    $match: {
      disease: "Type 2 Diabetes",
      "model.id": "mdl_diabetes_v2",
      "model.version": { $in: ["2.0.0", "2.1.0"] },
      computed_at: { $gte: ISODate("2026-03-01T00:00:00Z") }
    }
  },
  {
    $group: {
      _id: "$model.version",
      avg_risk_score: { $avg: "$risk_score" },
      avg_confidence: { $avg: "$confidence" },
      count: { $sum: 1 },
      high_risk_count: {
        $sum: { $cond: [{ $in: ["$risk_level", ["HIGH", "CRITICAL"]] }, 1, 0] }
      }
    }
  },
  {
    $project: {
      version: "$_id",
      _id: 0,
      avg_risk_score: { $round: ["$avg_risk_score", 3] },
      avg_confidence: { $round: ["$avg_confidence", 3] },
      count: 1,
      high_risk_pct: {
        $round: [{ $multiply: [{ $divide: ["$high_risk_count", "$count"] }, 100] }, 1]
      }
    }
  },
  { $sort: { version: 1 } }
]);

// ----------------------------------------------------------------------------
// 8. Korelasyon — HbA1c vs BMI (Descriptive İstatistik)
//
// API: POST /analysis/statistical { analysis_type: "CORRELATION" }
// patient_profile'daki rollup'ları kullanır.
// ----------------------------------------------------------------------------
print("\n--- 8. HbA1c ile BMI'nin descriptive istatistikleri ---");
db.patient_profile.aggregate([
  {
    $match: {
      "rollups.last_hba1c": { $exists: true, $ne: null },
      "rollups.bmi_latest": { $exists: true, $ne: null }
    }
  },
  {
    $group: {
      _id: null,
      n: { $sum: 1 },
      hba1c_avg: { $avg: "$rollups.last_hba1c" },
      hba1c_std: { $stdDevPop: "$rollups.last_hba1c" },
      bmi_avg: { $avg: "$rollups.bmi_latest" },
      bmi_std: { $stdDevPop: "$rollups.bmi_latest" },
      // Pearson korelasyon için cross-product
      sum_xy: {
        $sum: { $multiply: ["$rollups.last_hba1c", "$rollups.bmi_latest"] }
      },
      sum_x: { $sum: "$rollups.last_hba1c" },
      sum_y: { $sum: "$rollups.bmi_latest" }
    }
  },
  {
    $project: {
      _id: 0,
      n: 1,
      hba1c: { mean: "$hba1c_avg", std: "$hba1c_std" },
      bmi: { mean: "$bmi_avg", std: "$bmi_std" },
      // Covariance = E[XY] - E[X]E[Y]
      // Pearson r = Cov / (std_x * std_y)
      pearson_r: {
        $divide: [
          {
            $subtract: [
              { $divide: ["$sum_xy", "$n"] },
              { $multiply: [{ $divide: ["$sum_x", "$n"] }, { $divide: ["$sum_y", "$n"] }] }
            ]
          },
          { $multiply: ["$hba1c_std", "$bmi_std"] }
        ]
      }
    }
  }
]);

// ----------------------------------------------------------------------------
// İndeks → Sorgu Eşleme Tablosu (referans)
// ----------------------------------------------------------------------------
print("\n=== Sorgu - İndeks Eşlemesi ===");
print("Sorgu 1 → ix_disease_level_computed (risk_assessments)");
print("Sorgu 2 → ux_patient_param (lab_aggregates)");
print("Sorgu 3 → ix_gene_significance (genetic_profile)");
print("Sorgu 4 → ix_gender_birth_year + ix_chronic_icd10 (patient_profile)");
print("Sorgu 5 → ux_patient_id (patient_profile + lookup'lar)");
print("Sorgu 6 → ix_param_value (lab_aggregates)");
print("Sorgu 7 → ix_model_version_computed (risk_assessments)");
print("Sorgu 8 → coll-scan kabul edilebilir (descriptive stat full table tarar)");
