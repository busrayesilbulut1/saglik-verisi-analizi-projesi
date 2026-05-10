# Hafta 3 — İstatistiksel Analiz Modülü NoSQL Şeması

**Hazırlayan:** Sezer Çetinkaya

---

## Bu Paket Nedir?

Hafta 3'te bana atanan asıl görev olan **"İstatistiksel Analiz Modülü için NoSQL Veritabanı Şeması Tasarımı"** için hazırlanan teslim paketidir.


---

## Paket Yapısı

```
hafta3/
├── README.md                          ← bu dosya
├── 01_teknoloji_secimi.md             ← MongoDB vs Cassandra karar belgesi
├── 02_etl_eslestirmesi.md             ← PostgreSQL (Akın) → MongoDB mapping
├── 03_sema_tasarimi.md                ← 7 koleksiyonun doküman yapıları
├── 04_dogrulama_kurallari.js          ← $jsonSchema validator scriptleri
├── 05_indeksler.js                    ← createIndex scriptleri
├── 06_ornek_belgeler.json             ← Örnek dokümanlar (sentetik veri)
├── 07_sorgu_ornekleri.js              ← 8 adet aggregation pipeline örneği
└── 08_api_entegrasyon_haritasi.md     ← Melek'in REST endpoint'leri ↔ MongoDB koleksiyonları eşleştirmesi
```

### Okuma sırası

1. [01_teknoloji_secimi.md](01_teknoloji_secimi.md) — Neden MongoDB?
2. [02_etl_eslestirmesi.md](02_etl_eslestirmesi.md) — Akın'ın PostgreSQL şemasından nasıl beslenir?
3. [03_sema_tasarimi.md](03_sema_tasarimi.md) — 7 koleksiyonun yapısı
4. [04_dogrulama_kurallari.js](04_dogrulama_kurallari.js) — Veritabanı seviyesi validasyon
5. [05_indeksler.js](05_indeksler.js) — Sorgu kalıplarına uygun indeksler
6. [06_ornek_belgeler.json](06_ornek_belgeler.json) — Validator ve indekslere uyumlu örnek veri
7. [07_sorgu_ornekleri.js](07_sorgu_ornekleri.js) — Gerçek use case'ler için aggregation pipeline'lar
8. [08_api_entegrasyon_haritasi.md](08_api_entegrasyon_haritasi.md) — Hangi endpoint hangi koleksiyondan beslenir?

---

## Diğer Ekip Üyeleri ile İlişki

### Akın'ın PostgreSQL şeması (operasyonel katman)

Akın/projeakisi.md — 16 tablo, FK kısıtları, audit log.

- **Bu şema OLTP'dir** (Online Transaction Processing): hasta kaydı yazımı, doktor sorgusu, denetim takibi.
- Bizim NoSQL şeması bu kaynaktan **ETL ile beslenir** ve OLAP (Online Analytical Processing) görevini görür.
- Aynı veritabanını hem operasyonel hem analitik için kullanmak ölçeklenmez; bu sebeple iki katmanlı tasarım yapıldı.

### Melek'in API'si (tüketici katman)

melek/projeakisi.md — `/analysis`, `/prediction`, `/reports` endpoint'leri.

- Melek'in API'sinde her istatistiksel analiz çağrısı bu MongoDB koleksiyonlarından beslenir:
  - `POST /analysis/statistical` → `patient_profile` + `lab_aggregates` + `risk_assessments`
  - `POST /prediction/risk` → `feature_store` (model girişi) + `risk_assessments` (sonucun yazıldığı yer)
  - `GET /reports/visualizations/{patient_id}` → `lab_aggregates`, `risk_assessments`
- API'nin `chart_type` parametreleri (`TREND`, `RISK_GAUGE`, `LAB_HEATMAP`, `TIMELINE`) bu koleksiyonların 1-1 karşılığıdır.

### Mehmet'in pipeline'ı (kaynak temizleme)

Mehmet/projeakisi.md — `data_cleaning_pipeline_v2.py`

- Mehmet'in pipeline'ı CSV/JSON ham veriyi temizler ve KVKK anonimleştirme uygular.
- Pipeline çıktısı **Akın'ın PostgreSQL şemasına yazılır**, oradan bizim NoSQL'e ETL ile geçer.
- KVKK uyum stratejisi (`tc_kimlik_no` SHA-256 hash, salt + email/telefon) ETL aşamasında da korunur — bu MongoDB koleksiyonlarına ham PII alanları **hiç gelmez**.

---

## Tasarım Özeti

| Karar | Değer | Gerekçe |
|---|---|---|
| Teknoloji | MongoDB 7.0+ | Heterojen sağlık verisi + `$jsonSchema` + Aggregation Pipeline |
| Veritabanı adı | `saglik_analitik` | Akın'ın `saglik_db`'si ile karışmasın diye |
| Koleksiyon sayısı | 7 | OLTP'nin 16 tablosu denormalize + rollup'lı 7 koleksiyona indi |
| Patient ID formatı | `pt_[a-z0-9]{8}` | Melek'in API formatıyla bire bir |
| Senkronizasyon | Günlük batch (gece 03:00) | MVP için yeterli; CDC Hafta 6+ |
| KVKK | Ham PII MongoDB'ye gelmez | `tc_kimlik_no`, `email`, `telefon`, `ad`, `soyad` yasak |

### 7 Koleksiyon — Tek Satır Özeti

| Koleksiyon | Birincil Amaç |
|---|---|
| `patient_profile` | Dashboard'un ilk yüklediği hasta özeti + rollup'lar |
| `clinical_timeline` | Hasta kronolojik olay listesi (poliklinik, lab, MR vb.) |
| `lab_aggregates` | Pre-aggregated lab metrikleri (30g/90g/1y pencereli) |
| `genetic_profile` | Klinik öneme sahip genetik varyantlar (ham VCF HDFS'te) |
| `imaging_metadata` | DICOM metadata + radyolog raporu (ham görüntü HDFS'te) |
| `risk_assessments` | ML model çıktıları + öneriler (versiyonlu zaman serisi) |
| `feature_store` | ML modelleri için hazır feature vektörleri (TTL: 7 gün) |

---
