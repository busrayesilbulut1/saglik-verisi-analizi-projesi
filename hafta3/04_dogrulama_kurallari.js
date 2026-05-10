// ============================================================================
// Sağlık Analitik MongoDB Şeması — Validasyon Kuralları
// Hedef: MongoDB 7.0+
// Veritabanı: saglik_analitik
//
// Kullanım: mongosh < 04_dogrulama_kurallari.js
// (Veya scripti elle çalıştır: createCollection / collMod komutları idempotent değil,
//  yeniden çalıştırmadan önce ilgili koleksiyon mevcutsa drop edilmelidir.)
// ============================================================================

use("saglik_analitik");

// ----------------------------------------------------------------------------
// 1. patient_profile
// ----------------------------------------------------------------------------
db.createCollection("patient_profile", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "demographics", "meta"],
      properties: {
        patient_id: {
          bsonType: "string",
          pattern: "^pt_[a-z0-9]{8}$",
          description: "Hasta ID — Melek API formatı"
        },
        demographics: {
          bsonType: "object",
          required: ["birth_year", "gender"],
          properties: {
            birth_year: { bsonType: "int", minimum: 1900, maximum: 2026 },
            gender: { enum: ["M", "F", "OTHER"] },
            blood_type: { enum: ["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"] },
            city: { bsonType: "string", maxLength: 100 }
          }
        },
        chronic_conditions: {
          bsonType: "array",
          maxItems: 50,
          items: {
            bsonType: "object",
            required: ["icd10", "name"],
            properties: {
              icd10: { bsonType: "string", pattern: "^[A-Z][0-9]{2}(\\.[0-9]{1,2})?$" },
              name: { bsonType: "string", maxLength: 200 },
              diagnosed_at: { bsonType: "date" },
              severity: { enum: ["LOW", "MEDIUM", "HIGH"] }
            }
          }
        },
        allergies: {
          bsonType: "array",
          items: { bsonType: "string", maxLength: 100 }
        },
        rollups: {
          bsonType: "object",
          properties: {
            last_hba1c: { bsonType: "double", minimum: 0, maximum: 20 },
            last_hba1c_at: { bsonType: "date" },
            avg_systolic_30d: { bsonType: "double", minimum: 50, maximum: 300 },
            avg_diastolic_30d: { bsonType: "double", minimum: 30, maximum: 200 },
            bmi_latest: { bsonType: "double", minimum: 10, maximum: 80 },
            risk_scores: {
              bsonType: "object",
              additionalProperties: { bsonType: "double", minimum: 0, maximum: 1 }
            },
            last_updated: { bsonType: "date" }
          }
        },
        refs: {
          bsonType: "object",
          properties: {
            has_genetic_profile: { bsonType: "bool" },
            imaging_count: { bsonType: "int", minimum: 0 },
            latest_assessment_id: { bsonType: ["string", "null"] },
            timeline_event_count: { bsonType: "int", minimum: 0 }
          }
        },
        meta: {
          bsonType: "object",
          required: ["last_synced"],
          properties: {
            source_db: { bsonType: "string" },
            etl_version: { bsonType: "string" },
            last_synced: { bsonType: "date" }
          }
        }
      },
      // KVKK kontrol: yasak alanlar kabul edilmez
      additionalProperties: false
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// ----------------------------------------------------------------------------
// 2. clinical_timeline
// ----------------------------------------------------------------------------
db.createCollection("clinical_timeline", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "event_id", "event_type", "event_at"],
      properties: {
        patient_id: { bsonType: "string", pattern: "^pt_[a-z0-9]{8}$" },
        event_id: { bsonType: "string" },
        event_type: {
          enum: ["POLIKLINIK", "YATIS", "ACIL", "LAB", "IMAGING", "GENETIC"]
        },
        event_at: { bsonType: "date" },
        doctor_id_hash: {
          bsonType: "string",
          pattern: "^sha256:[a-f0-9]{64}$|^sha256:[a-f0-9]+$"
        },
        facility: { bsonType: "string", maxLength: 200 },
        complaint: { bsonType: "string", maxLength: 2000 },
        diagnoses: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["icd10", "name"],
            properties: {
              icd10: { bsonType: "string", pattern: "^[A-Z][0-9]{2}(\\.[0-9]{1,2})?$" },
              name: { bsonType: "string", maxLength: 200 }
            }
          }
        },
        prescriptions_summary: {
          bsonType: "object",
          properties: {
            prescription_count: { bsonType: "int", minimum: 0 },
            medication_count: { bsonType: "int", minimum: 0 },
            medications: { bsonType: "array", items: { bsonType: "string" } }
          }
        },
        notes_excerpt: { bsonType: "string", maxLength: 1000 },
        meta: { bsonType: "object" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// ----------------------------------------------------------------------------
// 3. lab_aggregates
// ----------------------------------------------------------------------------
db.createCollection("lab_aggregates", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "parameter", "windows", "latest"],
      properties: {
        patient_id: { bsonType: "string", pattern: "^pt_[a-z0-9]{8}$" },
        parameter: {
          bsonType: "object",
          required: ["code", "name", "unit"],
          properties: {
            code: { bsonType: "string", description: "LOINC kodu" },
            name: { bsonType: "string", maxLength: 200 },
            unit: { bsonType: "string", maxLength: 50 },
            reference_range: {
              bsonType: "object",
              properties: {
                min: { bsonType: "double" },
                max: { bsonType: "double" }
              }
            }
          }
        },
        windows: {
          bsonType: "object",
          properties: {
            "7d":  { bsonType: "object" },
            "30d": { bsonType: "object" },
            "90d": { bsonType: "object" },
            "1y":  { bsonType: "object" }
          }
        },
        latest: {
          bsonType: "object",
          required: ["value", "measured_at"],
          properties: {
            value: { bsonType: "double" },
            measured_at: { bsonType: "date" },
            is_abnormal: { bsonType: "bool" },
            abnormal_direction: { enum: ["HIGH", "LOW", null] }
          }
        },
        trend: {
          bsonType: "object",
          properties: {
            direction: { enum: ["INCREASING", "DECREASING", "STABLE"] },
            slope_per_month: { bsonType: "double" },
            last_updated: { bsonType: "date" }
          }
        },
        meta: { bsonType: "object" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// ----------------------------------------------------------------------------
// 4. genetic_profile
// ----------------------------------------------------------------------------
db.createCollection("genetic_profile", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "analysis_type", "analyzed_at"],
      properties: {
        patient_id: { bsonType: "string", pattern: "^pt_[a-z0-9]{8}$" },
        analysis_type: { enum: ["WGS", "WES", "SNP_PANEL", "PHARMACOGENOMICS"] },
        platform: { bsonType: "string", maxLength: 100 },
        analyzed_at: { bsonType: "date" },
        variants: {
          bsonType: "array",
          maxItems: 10000,
          items: {
            bsonType: "object",
            required: ["gene", "rsid", "clinical_significance"],
            properties: {
              gene: { bsonType: "string", maxLength: 50 },
              rsid: { bsonType: "string", pattern: "^rs[0-9]+$" },
              position: { bsonType: "string" },
              allele: { bsonType: "string", maxLength: 50 },
              clinical_significance: {
                enum: [
                  "PATHOGENIC",
                  "LIKELY_PATHOGENIC",
                  "VUS",
                  "LIKELY_BENIGN",
                  "BENIGN",
                  "RISK_FACTOR"
                ]
              },
              risk_score: { bsonType: "double", minimum: 0, maximum: 1 },
              conditions: { bsonType: "array", items: { bsonType: "string" } }
            }
          }
        },
        rollups: {
          bsonType: "object",
          properties: {
            total_variants_called: { bsonType: ["int", "long"], minimum: 0 },
            clinically_significant_count: { bsonType: "int", minimum: 0 },
            pathogenic_count: { bsonType: "int", minimum: 0 },
            likely_pathogenic_count: { bsonType: "int", minimum: 0 },
            vus_count: { bsonType: "int", minimum: 0 }
          }
        },
        raw_file: {
          bsonType: "object",
          properties: {
            hdfs_path: { bsonType: "string" },
            encryption_key_ref: { bsonType: "string" },
            file_size_bytes: { bsonType: ["int", "long"], minimum: 0 }
          }
        },
        meta: { bsonType: "object" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// ----------------------------------------------------------------------------
// 5. imaging_metadata
// ----------------------------------------------------------------------------
db.createCollection("imaging_metadata", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "dicom_uid", "modality", "captured_at", "hdfs_path"],
      properties: {
        patient_id: { bsonType: "string", pattern: "^pt_[a-z0-9]{8}$" },
        dicom_uid: { bsonType: "string", maxLength: 200 },
        modality: { enum: ["MRI", "CT", "X-RAY", "ULTRASOUND", "PET"] },
        body_part: { bsonType: "string", maxLength: 100 },
        captured_at: { bsonType: "date" },
        facility: { bsonType: "string", maxLength: 200 },
        hdfs_path: { bsonType: "string" },
        file_size_bytes: { bsonType: ["int", "long"], minimum: 0 },
        encryption_key_ref: { bsonType: "string" },
        radiologist_report: { bsonType: "string", maxLength: 10000 },
        ai_analysis: {
          bsonType: "object",
          properties: {
            model_version: { bsonType: "string" },
            findings: { bsonType: "array", items: { bsonType: "string" } },
            confidence: { bsonType: "double", minimum: 0, maximum: 1 },
            processed_at: { bsonType: "date" }
          }
        },
        meta: { bsonType: "object" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// ----------------------------------------------------------------------------
// 6. risk_assessments
// ----------------------------------------------------------------------------
db.createCollection("risk_assessments", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["assessment_id", "patient_id", "disease", "risk_score", "risk_level", "model", "computed_at"],
      properties: {
        assessment_id: { bsonType: "string", pattern: "^ras_[a-z0-9]+$" },
        patient_id: { bsonType: "string", pattern: "^pt_[a-z0-9]{8}$" },
        disease: { bsonType: "string", maxLength: 200 },
        risk_score: { bsonType: "double", minimum: 0, maximum: 1 },
        risk_level: { enum: ["LOW", "MEDIUM", "HIGH", "CRITICAL"] },
        confidence: { bsonType: "double", minimum: 0, maximum: 1 },
        prediction_horizon_months: { bsonType: "int", minimum: 1, maximum: 120 },
        model: {
          bsonType: "object",
          required: ["id", "version"],
          properties: {
            id: { bsonType: "string" },
            version: { bsonType: "string" },
            algorithm: { bsonType: "string" },
            trained_at: { bsonType: "date" }
          }
        },
        contributing_factors: {
          bsonType: "array",
          maxItems: 50,
          items: {
            bsonType: "object",
            required: ["factor", "importance"],
            properties: {
              factor: { bsonType: "string" },
              importance: { bsonType: "double", minimum: 0, maximum: 1 },
              direction: { enum: ["POSITIVE", "NEGATIVE", "NEUTRAL"] },
              value: {}                    // Heterojen — int, double, string
            }
          }
        },
        recommendations: {
          bsonType: "array",
          maxItems: 20,
          items: {
            bsonType: "object",
            required: ["type", "priority", "title"],
            properties: {
              type: { enum: ["LIFESTYLE", "MEDICATION", "SCREENING", "REFERRAL"] },
              priority: { enum: ["LOW", "MEDIUM", "HIGH"] },
              title: { bsonType: "string", maxLength: 200 },
              description: { bsonType: "string", maxLength: 2000 },
              evidence_level: { enum: ["A", "B", "C", "D"] }
            }
          }
        },
        computed_at: { bsonType: "date" },
        valid_until: { bsonType: "date" },
        meta: { bsonType: "object" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// ----------------------------------------------------------------------------
// 7. feature_store
// ----------------------------------------------------------------------------
db.createCollection("feature_store", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["patient_id", "feature_set", "features", "computed_at", "expires_at"],
      properties: {
        patient_id: { bsonType: "string", pattern: "^pt_[a-z0-9]{8}$" },
        feature_set: {
          bsonType: "object",
          required: ["id", "version"],
          properties: {
            id: { bsonType: "string" },
            version: { bsonType: "string" }
          }
        },
        features: {
          bsonType: "object",
          description: "Heterojen feature vektörü — model versiyonuna göre alanlar değişir"
        },
        computed_at: { bsonType: "date" },
        expires_at: { bsonType: "date" },
        meta: { bsonType: "object" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// ----------------------------------------------------------------------------
// Doğrulama: tüm koleksiyonların validator'larının yüklendiğini kontrol et
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

print("\n=== Validator Kurulum Kontrolü ===");
collections.forEach(name => {
  const info = db.getCollectionInfos({ name })[0];
  const hasValidator = info && info.options && info.options.validator;
  print(`${hasValidator ? "✓" : "✗"} ${name}`);
});
