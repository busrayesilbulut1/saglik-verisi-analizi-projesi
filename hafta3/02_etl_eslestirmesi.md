# 02 — ETL Mapping: PostgreSQL → MongoDB

## Genel Mimari

```
┌──────────────────────────┐         ┌────────────────────────┐
│  PostgreSQL (OLTP)       │  ETL    │  MongoDB (OLAP)        │
│  Akın'ın 16 tablosu      │ ──────▶ │  saglik_analitik       │
│  Operasyonel kayıtlar    │ günlük  │  7 koleksiyon          │
│  ACID, FK, audit         │ batch   │  Denormalize, esnek    │
└──────────────────────────┘         └────────────────────────┘
        ▲                                      ▲
        │                                      │
   Mehmet'in pipeline                   Melek'in API +
   (CSV → temiz veri)                   istatistiksel modül
```

## Veri Akışı (Üç Aşama)

1. **Ham veri → temiz veri:** Mehmet'in `data_cleaning_pipeline_v2.py` dosyası CSV/JSON ham veriyi temizler, KVKK anonimleştirme ve validasyon uygular.
2. **Temiz veri → PostgreSQL:** Akın'ın 16 tablolu şeması (Akın/projeakisi.md) operasyonel veri katmanı. Hasta kaydı, audit log, FK kısıtları burada.
3. **PostgreSQL → MongoDB:** Bu görevin tasarladığı katman. ETL job'ları PostgreSQL'i kaynak alır, denormalize eder ve 7 MongoDB koleksiyonuna yazar.

## Senkronizasyon Stratejisi

| Strateji | Tercih | Gerekçe |
|---|---|---|
| **Günlük batch** (gece 03:00) | ✅ Hafta 3 başlangıç | Basit, gözlenebilir, MVP için yeterli |
| **CDC (Change Data Capture)** | ⏳ Hafta 6+ | Debezium / logical replication ile gerçek zamanlıya yakın |
| **Trigger-based** | ❌ | PostgreSQL trigger'ları OLTP yükünü etkiler |

İlk sürümde **günlük batch** önerilir. Her gece tüm `tibbi_kayit`, `lab_sonuc`, `risk_degerlendirme` kayıtları taranır; son 24 saatte değişen hastalar için ilgili MongoDB dokümanı **upsert** edilir.

## Tablo → Koleksiyon Mapping

### Üst düzey eşleme

| MongoDB Koleksiyonu | Birincil Kaynak | Embed Edilen Tablolar | Denormalize Rollup'lar |
|---|---|---|---|
| `patient_profile` | `hasta` | tani (kronik), hasta_onayi (sayım) | last_hba1c, avg_systolic_30d, latest_risk_score |
| `clinical_timeline` | `tibbi_kayit` | tani, ilac_recete (özet) | event_count_per_year |
| `lab_aggregates` | `lab_test + lab_sonuc` | — | min/max/avg per parametre, 30g/90g/1y pencereler |
| `genetic_profile` | `genetik_profil` | genetik_varyant (array) | high_risk_variant_count |
| `imaging_metadata` | `tibbi_goruntu` | — | (binary HDFS'te kalır, sadece path tutulur) |
| `risk_assessments` | `risk_degerlendirme` | oneri (array) | recommendation_count |
| `feature_store` | (hesaplanır) | — | ML feature vektörü, model versiyonuna bağlı |

### Detaylı alan mapping'i

#### `patient_profile`

| MongoDB Yolu | PostgreSQL Kaynağı | Tip | Notlar |
|---|---|---|---|
| `patient_id` | `hasta.hasta_id` | UUID → string | `pt_` öneki + ilk 8 karakter |
| `demographics.birth_year` | YEAR(`hasta.dogum_tarihi`) | int | Tam tarih KVKK gizliliği için yıla indirgenir |
| `demographics.gender` | `hasta.cinsiyet` | enum | M/F/OTHER |
| `demographics.blood_type` | `hasta.kan_grubu` | enum | A+/A-/B+/B-/AB+/AB-/0+/0- |
| `chronic_conditions[]` | `tani` WHERE aktif=true AND siddet IN (...) | array | ICD-10 kodu + ad |
| `allergies[]` | (Akın'ın şemasında ayrı tablo yok — `tibbi_kayit.tedavi_notu` NLP veya manuel) | array | İleride ayrı tablo gerekebilir |
| `rollups.last_hba1c` | son `lab_sonuc` WHERE parametre_adi='HbA1c' | double | ETL hesaplar |
| `rollups.avg_systolic_30d` | avg(`lab_sonuc.deger`) son 30 gün | double | ETL hesaplar |
| `rollups.latest_risk_score` | son `risk_degerlendirme.risk_skoru` | double | hastalik_adi başına ayrı alan |
| `refs.has_genetic_profile` | EXISTS(`genetik_profil` WHERE hasta_id=...) | bool | Sorguyu hızlandırır |
| `meta.last_synced` | ETL job timestamp | datetime | UTC |

#### `clinical_timeline`

| MongoDB Yolu | PostgreSQL Kaynağı | Tip | Notlar |
|---|---|---|---|
| `_id` | (ObjectId) | ObjectId | Otomatik |
| `patient_id` | `tibbi_kayit.hasta_id` | string | |
| `event_id` | `tibbi_kayit.kayit_id` | string | |
| `event_type` | `tibbi_kayit.kayit_turu` | enum | POLIKLINIK/YATIS/ACIL |
| `event_at` | `tibbi_kayit.ziyaret_tarihi` | datetime | |
| `doctor_id_hash` | SHA256(`tibbi_kayit.doktor_id`) | string | KVKK pseudonimleştirme |
| `complaint` | `tibbi_kayit.sikayet` | string | Serbest metin |
| `diagnoses[]` | `tani` WHERE kayit_id=... | array | icd10_kodu + tani_adi |
| `prescriptions_summary` | count(`ilac_recete`) + count(`ilac_kalemi`) | object | Detay reçete tablosunda kalır |

#### `lab_aggregates`

| MongoDB Yolu | PostgreSQL Kaynağı | Tip | Notlar |
|---|---|---|---|
| `patient_id` | `lab_test.hasta_id` | string | |
| `parameter_code` | `lab_sonuc.parametre_adi` (LOINC) | string | LOINC kodu hedef |
| `unit` | `lab_sonuc.birim` | string | |
| `windows.30d` | {min, max, avg, count} son 30 gün | object | ETL hesaplar |
| `windows.90d` | {min, max, avg, count} son 90 gün | object | ETL hesaplar |
| `windows.1y` | {min, max, avg, count} son 1 yıl | object | ETL hesaplar |
| `latest.value` | en son `lab_sonuc.deger` | double | |
| `latest.measured_at` | en son `lab_sonuc.numune_tarihi` | datetime | |
| `latest.is_abnormal` | latest.value < ref_min OR > ref_max | bool | ETL hesaplar |

#### `genetic_profile`

| MongoDB Yolu | PostgreSQL Kaynağı | Tip | Notlar |
|---|---|---|---|
| `patient_id` | `genetik_profil.hasta_id` | string | |
| `analysis_type` | `genetik_profil.analiz_turu` | enum | WGS/WES/SNP_PANEL |
| `analyzed_at` | `genetik_profil.analiz_tarihi` | date | |
| `variants[]` | `genetik_varyant` WHERE profil_id=... | array | EMBED — tipik 100-10K varyant |
| `variants[].gene` | `genetik_varyant.gen_adi` | string | |
| `variants[].rsid` | `genetik_varyant.rsid` | string | |
| `variants[].clinical_significance` | `genetik_varyant.klinik_onemi` | enum | PATHOGENIC/BENIGN/VUS |
| `variants[].risk_score` | `genetik_varyant.risk_skoru` | double | |
| `rollups.high_risk_variant_count` | count(WHERE klinik_onemi='Patojenik') | int | |
| `raw_file_path` | `genetik_profil.depolama_yolu` | string | HDFS yolu, ham dosya orada |

#### `imaging_metadata`

| MongoDB Yolu | PostgreSQL Kaynağı | Tip | Notlar |
|---|---|---|---|
| `patient_id` | `tibbi_goruntu.hasta_id` | string | |
| `dicom_uid` | `tibbi_goruntu.dicom_uid` | string | unique |
| `modality` | `tibbi_goruntu.goruntu_turu` | enum | MRI/CT/X-RAY/ULTRASOUND |
| `captured_at` | `tibbi_goruntu.cekim_tarihi` | datetime | |
| `hdfs_path` | `tibbi_goruntu.depolama_yolu` | string | Ham DICOM burada |
| `radiologist_report` | `tibbi_goruntu.radyolog_raporu` | string | Text indeksi için |
| `encryption_key_ref` | `tibbi_goruntu.sifreleme_anahtari` | string | KMS referansı |

#### `risk_assessments`

| MongoDB Yolu | PostgreSQL Kaynağı | Tip | Notlar |
|---|---|---|---|
| `assessment_id` | `risk_degerlendirme.degerlendirme_id` | string | |
| `patient_id` | `risk_degerlendirme.hasta_id` | string | |
| `disease` | `risk_degerlendirme.hastalik_adi` | string | |
| `risk_score` | `risk_degerlendirme.risk_skoru` | double | 0.0 - 1.0 |
| `risk_level` | `risk_degerlendirme.risk_kategorisi` | enum | LOW/MEDIUM/HIGH/CRITICAL |
| `model_version` | `risk_degerlendirme.model_versiyonu` | string | mdl_diabetes_v2.1.0 |
| `computed_at` | `risk_degerlendirme.hesaplama_tarihi` | datetime | |
| `recommendations[]` | `oneri` WHERE degerlendirme_id=... | array | EMBED — küçük, birlikte okunur |
| `contributing_factors[]` | (model çıktısı SHAP/feature importance) | array | Modelden gelir |

#### `feature_store`

| MongoDB Yolu | Kaynak | Tip | Notlar |
|---|---|---|---|
| `patient_id` | (hesaplanır) | string | |
| `feature_set_version` | model adı + versiyon | string | "diabetes_v2.1" |
| `features` | (hesaplanır) | object | key-value, ML için hazır vektör |
| `features.age` | YEAR(now) - birth_year | int | |
| `features.bmi` | son ölçüm | double | |
| `features.hba1c` | rollups.last_hba1c | double | |
| `features.has_brca1_pathogenic` | EXISTS variant | bool | |
| `computed_at` | ETL job zamanı | datetime | |
| `expires_at` | computed_at + 7 gün | datetime | TTL indeksi |

## KVKK / Gizlilik Kuralları

ETL aşamasında **kesinlikle** uygulanacaklar:

1. `hasta.tc_kimlik_no` → MongoDB'ye **gönderilmez.** Sadece `patient_id` (sistem üretimi UUID öneki) taşınır.
2. `hasta.email`, `hasta.telefon` → MongoDB'ye **gönderilmez.** Bu alanlar OLTP'de kalır, analitik için gerekli değil.
3. `hasta.ad`, `hasta.soyad` → MongoDB'ye **gönderilmez.** İsim asla analitik depoda olmamalı.
4. `hasta.dogum_tarihi` → tam tarih yerine **birth_year** olarak indirgenir. Yaş hesaplaması için yeterli, kimlik tespitini zorlaştırır.
5. `doktor_id` → SHA-256 hash + ortak salt ile pseudonimleştirilir. Audit gerekirse OLTP'den geri çözülür.