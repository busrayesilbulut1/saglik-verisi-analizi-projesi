# API — MongoDB Entegrasyon Haritası

Bu belge, Melek'in REST API tasarımındaki (melek/projeakisi.md) endpoint'lerin
hangisinin Sezer'in MongoDB koleksiyonlarından besleneceğini gösterir.
Amaç: iki üyenin çalışmalarının entegrasyon noktasını yazılı hale getirmek.

---

## Karar Notu

Melek'in API belgesinin "Açık Sorular" bölümü (Bölüm 10, Madde 2) MongoDB/Cassandra/HBase
tercihini hâlâ beklemede göstermektedir. Bu karar Hafta 3'te Sezer tarafından alınmıştır:
**MongoDB 7.0+ seçildi** — gerekçe: [01_teknoloji_secimi.md](01_teknoloji_secimi.md).

---

## Koleksiyon → Endpoint Haritası

### `patient_profile`

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/patients` | `POST` | Yeni hasta kaydı → `patient_profile` dokümanı oluşturur |
| `/patients/{patient_id}` | `GET` | Hasta demografisi, kronik durumlar, alerjiler, rollup'lar |
| `/patients/{patient_id}` | `PATCH` | Kronik durum / alerji güncellemesi |
| `/patients` | `GET` | Hasta listesi; `gender` ve `condition` filtreleri `demographics` ve `chronic_conditions` alanlarını sorgular |

**Sağlanan alanlar:** `patient_id`, `birth_year`, `gender`, `blood_type`, `chronic_conditions`, `allergies`, `risk_scores` (rollup).

---

### `clinical_timeline`

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/data/{patient_id}/history` | `GET` | Kronik muayene, tanı, ilaç geçmişi; `record_type` filtresiyle döner |
| `/reports/visualizations/{patient_id}` | `GET` | `chart_type=TIMELINE` → klinik olayların kronolojik listesi |

**Sağlanan alanlar:** `events[]` (tip, tarih, kaynak sistem, içerik).

---

### `lab_aggregates`

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/reports/visualizations/{patient_id}` | `GET` | `chart_type=TREND` → `metric` ve `period` parametrelerine göre zaman serisi döner |
| `/reports/visualizations/{patient_id}` | `GET` | `chart_type=LAB_HEATMAP` → korelasyon hesabı için çoklu metrik değerleri döner |
| `/analysis/statistical` | `POST` | `record_types: ["LAB"]` kapsamında pre-aggregated değerler kullanılır |

**Sağlanan alanlar:** `windows.7d`, `windows.30d`, `windows.90d`, `windows.1y` (min/max/avg); `test_name`, `unit`, `reference_range`.

---

### `risk_assessments`

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/prediction/risk` | `POST` | Tahmin sonucu bu koleksiyona yazılır; `prediction_id`, `risk_score`, `risk_level`, `contributing_factors` döner |
| `/prediction/history/{patient_id}` | `GET` | Geçmiş tahminler zaman serisi olarak döner |
| `/prediction/recommendations` | `POST` | `prediction_id` üzerinden bu koleksiyondan risk bağlamı okunur; öneri üretilir |
| `/reports/visualizations/{patient_id}` | `GET` | `chart_type=RISK_GAUGE` → güncel `risk_score` ve `risk_level` döner |
| `/reports/generate` | `POST` | `include_sections: ["RISK_SCORES"]` → risk zaman serisi rapora dahil edilir |

**Sağlanan alanlar:** `risk_score` (0-1), `risk_level` (LOW/MEDIUM/HIGH/CRITICAL), `contributing_factors[]`, `recommendations[]`, `valid_until`.

---

### `genetic_profile`

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/data/genetic` | `POST` | Genetik dosya yüklenir → ETL işleyerek bu koleksiyona yazar |
| `/prediction/risk` | `POST` | `include_data_types: ["GENETIC"]` → genetik varyantlar feature olarak kullanılır |

**Sağlanan alanlar:** `panel_type`, `pathogenic_variants[]` (gen, varyant, klinik önem), `sequenced_at`.

---

### `imaging_metadata`

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/data/imaging` | `POST` | DICOM/görüntü yüklenir → ETL metadata'yı bu koleksiyona yazar; ham dosya HDFS'te kalır |
| `/data/{patient_id}/history` | `GET` | `record_type=IMAGING` filtresiyle görüntü geçmişi döner |

**Sağlanan alanlar:** `modality`, `body_part`, `dicom_path` (HDFS referansı), `radiologist_report`, `recorded_at`.

---

### `feature_store`

| Endpoint | Metod | Açıklama |
|---|---|---|
| `/prediction/risk` | `POST` | ML modeli bu koleksiyondaki hazır feature vektörünü kullanır; eksikse ETL tetikler |

**Sağlanan alanlar:** Hasta başına tek feature vektörü; TTL: 7 gün (otomatik silinir, her tahmin öncesi yenilenir).

---

## Özet Tablo

| MongoDB Koleksiyonu | Beslediği Modüller | Kritiklik |
|---|---|---|
| `patient_profile` | Hasta Yönetimi (`/patients`) | Yüksek — tüm hasta işlemlerinin merkezi |
| `clinical_timeline` | Veri Yükleme (`/data`), Görselleştirme | Yüksek — kronolojik hasta geçmişi |
| `lab_aggregates` | Analiz (`/analysis`), Görselleştirme | Yüksek — TREND ve HEATMAP grafikleri |
| `risk_assessments` | Tahmin (`/prediction`), Raporlama | Kritik — doktor kararlarının dayandığı çıktı |
| `genetic_profile` | Veri Yükleme (`/data`), Tahmin | Orta — tahmin kalitesini artırır |
| `imaging_metadata` | Veri Yükleme (`/data`) | Orta — DICOM metadata indeksi |
| `feature_store` | Tahmin (`/prediction`) | Yüksek — ML inference hızı için önbellek |

---

## Açık Koordinasyon Noktaları

1. **`/data/records` → `clinical_timeline` yazma zamanlaması:** API `POST /data/records` isteği aldığında ETL hemen mi çalışır yoksa gece batch'e mi eklenir? Gerçek zamanlı kayıt ihtiyacı varsa ETL mimarisi güncellenmeli.
2. **`/analysis/statistical` veri kapsamı:** `dataset_scope.patient_ids` listesi büyükse `lab_aggregates` pre-aggregated değerleri yeterli olmayabilir; ham `lab_sonuc` tablosuna erişim gerekebilir.
3. **`feature_store` TTL yönetimi:** 7 günlük TTL ile `/prediction/risk` tetiklenme sıklığı uyumlu mu? Sık tahmin yapılıyorsa TTL kısaltılabilir.
