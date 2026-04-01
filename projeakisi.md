# Bayt Bükücüler - Proje Akışı ve Haftalık İlerleme

Bu dosya Bayt Bükücüler takımının haftalık proje ilerlemesini ve görev dağılımını içerir.

## Proje
Sağlık Verisi Analizi ve Tahminleme Sistemi

## Takım
- Büşra Yeşilbulut (Scrum Master)
- Akın Ağaçbacak
- Sezer Çetinkaya
- Melek Şimşek
- Mehmet Boztepe

---

## 1. Hafta (9-15 Mart)
**Büşra Yeşilbulut**: GitHub repo oluşturuldu ve proje akışı dokümanı hazırlandı.
**Akın Ağaçbacak**: Veri kaynakları araştırması.
**Sezer Çetinkaya**: Makine öğrenmesi algoritmaları araştırması.
**Melek Şimşek**: Veri temizleme yöntemleri araştırması.

# Sağlık Verisi Analizi ve Tahminleme Sistemi
## Gerekli Teknolojilerin Araştırılması

### Proje Görevi
Bu görev kapsamında proje için gerekli olan teknolojiler araştırılmıştır. Veri işleme araçları, analitik platformlar, programlama dilleri ve makine öğrenmesi frameworkleri incelenmiş; her bir teknolojinin avantaj ve dezavantajları karşılaştırılarak proje için en uygun teknolojiler belirlenmiştir.

---

# 1. Proje Genel Tanımı

**Sağlık Verisi Analizi ve Tahminleme Sistemi**, hasta kayıtları, tıbbi görüntüleme verileri ve genetik bilgileri analiz ederek hastalık risklerini tahmin etmeyi amaçlayan bir sistemdir. Ayrıca sistem, kişiselleştirilmiş tedavi önerileri sunarak erken teşhis ve daha etkili tedavi yöntemleri geliştirilmesine katkı sağlamayı hedeflemektedir.

Bu tür bir sistem için aşağıdaki teknoloji alanları gereklidir:

- Programlama dilleri
- Veri işleme teknolojileri
- Makine öğrenmesi ve yapay zeka araçları
- Tıbbi görüntü işleme araçları
- Veri görselleştirme araçları
- Bulut altyapısı

---

# 2. Programlama Dilleri

## Python

Python, veri bilimi, makine öğrenmesi ve yapay zeka projelerinde en çok kullanılan programlama dillerinden biridir.

### Avantajları

- NumPy, Pandas ve Scikit-learn gibi güçlü veri analizi kütüphanelerine sahiptir
- Makine öğrenmesi ve yapay zeka projeleri için geniş ekosistem sunar
- Öğrenmesi ve kullanması görece kolaydır

### Dezavantajları

- Bazı performans gerektiren işlemlerde diğer dillere göre daha yavaş olabilir
- Büyük sistemlerde optimizasyon gerekebilir

---

## R

R dili özellikle istatistiksel analiz ve veri görselleştirme için geliştirilmiş bir programlama dilidir.

### Avantajları

- Güçlü istatistiksel analiz araçlarına sahiptir
- Akademik araştırmalarda yaygın olarak kullanılmaktadır
- Veri görselleştirme konusunda oldukça güçlüdür

### Dezavantajları

- Büyük ölçekli yazılım projeleri için sınırlı kullanım
- Python kadar geniş bir yazılım geliştirme ekosistemine sahip değildir

---

# 3. Veri İşleme Teknolojileri

## Apache Spark

Apache Spark, büyük veri setlerini işlemek için kullanılan dağıtık veri işleme platformudur.

### Avantajları

- Büyük veri setlerini hızlı şekilde işleyebilir
- Gerçek zamanlı veri analizini destekler
- Makine öğrenmesi için yerleşik araçlara sahiptir

### Dezavantajları

- Kurulumu ve yönetimi karmaşık olabilir
- Küçük projelerde gereksiz olabilir

---

## Apache Hadoop

Hadoop, büyük veri depolama ve işleme için kullanılan açık kaynaklı bir frameworktür.

### Avantajları

- Çok büyük veri setlerini depolayabilir
- Dağıtık sistemlerde çalışabilir
- Ölçeklenebilir bir mimariye sahiptir

### Dezavantajları

- Gerçek zamanlı analiz için Spark kadar hızlı değildir
- Kurulum ve yönetim süreci karmaşık olabilir

---

# 4. Makine Öğrenmesi Frameworkleri

## TensorFlow

TensorFlow, Google tarafından geliştirilen açık kaynaklı bir makine öğrenmesi frameworküdür.

### Avantajları

- Derin öğrenme modelleri için güçlü altyapı sağlar
- GPU ve dağıtık sistem desteği sunar
- Tıbbi görüntü analizi gibi alanlarda yaygın olarak kullanılmaktadır

### Dezavantajları

- Öğrenme süreci başlangıç seviyesinde zor olabilir
- Basit projelerde fazla karmaşık olabilir

---

## Scikit-learn

Scikit-learn Python tabanlı popüler bir makine öğrenmesi kütüphanesidir.

### Avantajları

- Kullanımı oldukça kolaydır
- Sınıflandırma, regresyon ve kümeleme algoritmaları içerir
- Geniş topluluk desteğine sahiptir

### Dezavantajları

- Derin öğrenme modelleri için uygun değildir
- GPU desteği sınırlıdır

---

# 5. Tıbbi Görüntü İşleme Araçları

## MONAI

MONAI (Medical Open Network for AI), tıbbi görüntü analizi için geliştirilmiş açık kaynaklı bir derin öğrenme frameworküdür.

### Avantajları

- Sağlık sektöründeki görüntü analizi problemleri için optimize edilmiştir
- Görüntü segmentasyonu ve sınıflandırma destekler
- PyTorch tabanlıdır

### Dezavantajları

- Derin öğrenme bilgisi gerektirir
- Yüksek donanım gereksinimi olabilir

---

# 6. Veri Görselleştirme Araçları

## Tableau

Tableau, veri görselleştirme ve dashboard oluşturma için kullanılan bir platformdur.

### Avantajları

- Kullanıcı dostu arayüze sahiptir
- Etkileşimli veri panelleri oluşturulabilir
- Büyük veri setleri kolayca görselleştirilebilir

### Dezavantajları

- Lisans maliyeti olabilir
- Kod tabanlı projelerle entegrasyonu sınırlı olabilir

---

# 7. Bulut Platformları

## Microsoft Azure

Microsoft Azure veri depolama, analiz ve yapay zeka geliştirme için kullanılan bir bulut platformudur.

### Avantajları

- Ölçeklenebilir altyapı sağlar
- Yapay zeka ve veri analizi servisleri içerir
- Güvenli veri depolama imkanı sunar

### Dezavantajları

- Kullanıma bağlı maliyet oluşabilir
- Bulut altyapısı yönetimi teknik bilgi gerektirir

---

# 8. Önerilen Teknoloji Yığını

Yapılan araştırmalar sonucunda proje için aşağıdaki teknoloji kombinasyonu önerilmektedir:

| Bileşen | Önerilen Teknoloji |
|--------|-------------------|
| Programlama Dili | Python |
| Veri İşleme | Apache Spark |
| Makine Öğrenmesi | TensorFlow / Scikit-learn |
| Tıbbi Görüntü Analizi | MONAI |
| Veri Görselleştirme | Tableau |
| Bulut Platformu | Microsoft Azure |

---

# 9. Sonuç

Sağlık verisi analizi sistemleri; büyük veri teknolojileri, makine öğrenmesi ve bulut altyapısının birlikte kullanılmasını gerektirir. Python tabanlı geliştirme ortamı, Spark ile veri işleme, TensorFlow ile makine öğrenmesi ve MONAI ile tıbbi görüntü analizi kullanılarak güçlü bir sağlık tahminleme sistemi oluşturulabilir.

Bu teknolojiler sayesinde hastalık riskleri daha erken tespit edilebilir ve kişiselleştirilmiş tedavi süreçleri desteklenebilir.
**Mehmet Boztepe**: Sağlık veri setleri araştırması.

---

## 2. Hafta
İlerleyen haftalarda doldurulacaktır.

---
## 3. Hafta
# Sağlık Verisi Analizi ve Tahminleme Sistemi — API Tasarım Dokümanı


---

## İçindekiler

1. [Genel Bakış](#1-genel-bakış)
2. [Temel Prensipler](#2-temel-prensipler)
3. [Kimlik Doğrulama ve Yetkilendirme](#3-kimlik-doğrulama-ve-yetkilendirme)
4. [Standart Yanıt Formatları](#4-standart-yanıt-formatları)
5. [Hata Kodları](#5-hata-kodları)
6. [Modüller ve Endpoint'ler](#6-modüller-ve-endpointler)
   - 6.1 [Hasta Yönetimi](#61-hasta-yönetimi)
   - 6.2 [Veri Yükleme](#62-veri-yükleme)
   - 6.3 [Analiz ve Modelleme](#63-analiz-ve-modelleme)
   - 6.4 [Risk Tahmini ve Öneri](#64-risk-tahmini-ve-öneri)
   - 6.5 [Raporlama ve Görselleştirme](#65-raporlama-ve-görselleştirme)
7. [Veri Güvenliği ve Gizlilik](#7-veri-güvenliği-ve-gizlilik)
8. [Rate Limiting](#8-rate-limiting)
9. [Versiyonlama Stratejisi](#9-versiyonlama-stratejisi)
10. [Açık Sorular ve Kararlar](#10-açık-sorular-ve-kararlar)

---

## 1. Genel Bakış

Bu doküman, Sağlık Verisi Analizi ve Tahminleme Sistemi'nin dış dünyayla iletişimini sağlayacak RESTful API'lerin tasarımını tanımlar. Sistem; hasta kayıtları, tıbbi görüntüleme verileri ve genetik bilgileri analiz ederek hastalık risklerini tahmin etmekte ve kişiselleştirilmiş tedavi önerileri sunmaktadır.

**Base URL:**
```
https://api.saglik-sistem.com/v1
```

**Desteklenen Format:** JSON  
**Karakter Kodlaması:** UTF-8  
**Protokol:** HTTPS (zorunlu)

---

## 2. Temel Prensipler

| Prensip | Açıklama |
|---|---|
| REST mimarisi | Kaynak odaklı URL yapısı, standart HTTP metodları |
| Durumsuzluk (Stateless) | Her istek kendi başına tüm bilgiyi taşır |
| Tutarlılık | Tüm endpoint'lerde aynı isim ve format kuralları |
| Güvenlik önce | Tüm iletişim şifrelenmiş, her erişim loglanır |
| Gizlilik | Kişisel sağlık verisi (PHI) maskelenerek iletilir |

**HTTP Metod Kullanımı:**

| Metod | Kullanım |
|---|---|
| `GET` | Veri okuma |
| `POST` | Yeni kayıt oluşturma / işlem tetikleme |
| `PUT` | Kaydın tamamını güncelleme |
| `PATCH` | Kaydın bir kısmını güncelleme |
| `DELETE` | Kayıt silme (soft delete) |

---

## 3. Kimlik Doğrulama ve Yetkilendirme

### 3.1 Kimlik Doğrulama

Sistem **OAuth 2.0 + JWT (JSON Web Token)** kullanır.

**Token alma:**
```
POST /auth/token
```

**Request Body:**
```json
{
  "client_id": "string",
  "client_secret": "string",
  "grant_type": "client_credentials"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Tüm isteklerde header:**
```
Authorization: Bearer <access_token>
```

### 3.2 Rol Tabanlı Erişim (RBAC)

| Rol | Açıklama | Erişim |
|---|---|---|
| `ADMIN` | Sistem yöneticisi | Tüm endpoint'ler |
| `DOCTOR` | Doktor / Hekim | Hasta verileri, tahmin, rapor |
| `ANALYST` | Veri analisti | Analiz, modelleme, rapor (anonim veri) |
| `PATIENT` | Hasta | Yalnızca kendi verisi |
| `READONLY` | Salt okunur | Yalnızca GET istekleri |

---

## 4. Standart Yanıt Formatları

### 4.1 Başarılı Yanıt

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "timestamp": "2026-03-30T10:00:00Z",
    "request_id": "req_abc123",
    "version": "1.0"
  }
}
```

### 4.2 Liste Yanıtı (Sayfalama ile)

```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_records": 150,
    "total_pages": 8
  },
  "meta": {
    "timestamp": "2026-03-30T10:00:00Z",
    "request_id": "req_abc123"
  }
}
```
Bu format, büyük veri listelerinde sayfalama (pagination) desteği sağlar.

### 4.3 Hata Yanıtı

```json
{
  "success": false,
  "error": {
    "code": "PATIENT_NOT_FOUND",
    "message": "Belirtilen hasta kaydı bulunamadı.",
    "details": { ... }
  },
  "meta": {
    "timestamp": "2026-03-30T10:00:00Z",
    "request_id": "req_abc123"
  }
}
```

---

## 5. Hata Kodları

### HTTP Durum Kodları

| Kod | Anlam | Kullanım |
|---|---|---|
| `200` | OK | Başarılı GET, PUT, PATCH |
| `201` | Created | Başarılı POST (yeni kayıt) |
| `202` | Accepted | Uzun süren işlem kuyruğa alındı |
| `400` | Bad Request | Geçersiz istek, eksik alan |
| `401` | Unauthorized | Token yok veya geçersiz |
| `403` | Forbidden | Yetki yok |
| `404` | Not Found | Kaynak bulunamadı |
| `409` | Conflict | Çakışma (örn. mükerrer kayıt) |
| `422` | Unprocessable Entity | Validasyon hatası |
| `429` | Too Many Requests | Rate limit aşıldı |
| `500` | Internal Server Error | Sunucu hatası |

### Uygulama Hata Kodları

| Kod | Açıklama |
|---|---|
| `PATIENT_NOT_FOUND` | Hasta kaydı bulunamadı |
| `DUPLICATE_PATIENT` | Aynı kimlik bilgisiyle kayıt mevcut |
| `INVALID_FILE_FORMAT` | Desteklenmeyen dosya formatı |
| `FILE_SIZE_EXCEEDED` | Dosya boyutu limiti aşıldı |
| `ANALYSIS_NOT_READY` | Analiz sonucu henüz hazır değil |
| `MODEL_UNAVAILABLE` | İstenen model şu an kullanılamıyor |
| `INSUFFICIENT_DATA` | Tahmin için yeterli veri yok |
| `AUTH_TOKEN_EXPIRED` | Token süresi dolmuş |
| `PERMISSION_DENIED` | Bu veriye erişim yetkiniz yok |
| `RATE_LIMIT_EXCEEDED` | İstek limiti aşıldı |

---

## 6. Modüller ve Endpoint'ler

---

### 6.1 Hasta Yönetimi

**Base path:** `/patients`

#### `POST /patients` — Yeni Hasta Kaydı Oluştur

**Yetki:** `ADMIN`, `DOCTOR`

**Request Body:**
```json
{
  "national_id_hash": "string (SHA-256 hash)",
  "birth_year": 1985,
  "gender": "M | F | OTHER",
  "blood_type": "A+ | A- | B+ | B- | AB+ | AB- | 0+ | 0-",
  "contact": {
    "email_hash": "string (SHA-256 hash)",
    "phone_hash": "string (SHA-256 hash)"
  },
  "chronic_conditions": ["DIABETES", "HYPERTENSION"],
  "allergies": ["PENICILLIN"]
}
```

**Response `201`:**
```json
{
  "success": true,
  "data": {
    "patient_id": "pt_7f3a9b2c",
    "created_at": "2026-03-30T10:00:00Z",
    "status": "ACTIVE"
  }
}
```

> **Gizlilik Notu:** TC kimlik numarası ve iletişim bilgileri API'ye ham olarak gönderilmez; istemci tarafında SHA-256 hash'lenerek iletilir.

---

#### `GET /patients/{patient_id}` — Hasta Bilgisi Getir

**Yetki:** `ADMIN`, `DOCTOR`, `PATIENT` (yalnızca kendi verisi)

**Path Parametresi:**
- `patient_id` (string, zorunlu)

**Response `200`:**
```json
{
  "success": true,
  "data": {
    "patient_id": "pt_7f3a9b2c",
    "birth_year": 1985,
    "gender": "M",
    "blood_type": "A+",
    "chronic_conditions": ["DIABETES"],
    "allergies": ["PENICILLIN"],
    "created_at": "2026-03-30T10:00:00Z",
    "last_updated": "2026-03-30T10:00:00Z"
  }
}
```

---

#### `PATCH /patients/{patient_id}` — Hasta Bilgisi Güncelle

**Yetki:** `ADMIN`, `DOCTOR`

**Request Body:** (yalnızca güncellenmek istenen alanlar)
```json
{
  "chronic_conditions": ["DIABETES", "HYPERTENSION"],
  "allergies": ["PENICILLIN", "ASPIRIN"]
}
```

**Response `200`:** Güncellenmiş hasta objesi döner.

---

#### `GET /patients` — Hasta Listesi

**Yetki:** `ADMIN`, `DOCTOR`

**Query Parametreleri:**

| Parametre | Tip | Açıklama |
|---|---|---|
| `page` | int | Sayfa numarası (default: 1) |
| `page_size` | int | Sayfa başı kayıt (default: 20, max: 100) |
| `gender` | string | Filtre: M, F, OTHER |
| `condition` | string | Filtre: kronik hastalık kodu |

---

#### `DELETE /patients/{patient_id}` — Hasta Kaydını Sil (Soft Delete)

**Yetki:** `ADMIN`

**Response `200`:**
```json
{
  "success": true,
  "data": {
    "patient_id": "pt_7f3a9b2c",
    "status": "DELETED",
    "deleted_at": "2026-03-30T10:00:00Z"
  }
}
```

---

### 6.2 Veri Yükleme

**Base path:** `/data`

#### `POST /data/records` — Tıbbi Kayıt Yükle

**Yetki:** `ADMIN`, `DOCTOR`

**Request Body:**
```json
{
  "patient_id": "pt_7f3a9b2c",
  "record_type": "LAB | IMAGING | GENETIC | CLINICAL_NOTE | VITAL_SIGNS",
  "recorded_at": "2026-03-28T08:30:00Z",
  "source_system": "string (ör: HIS_ISTANBUL_TIP)",
  "payload": { ... }
}
```

**`payload` — LAB örneği:**
```json
{
  "test_name": "HbA1c",
  "value": 7.2,
  "unit": "%",
  "reference_range": { "min": 4.0, "max": 5.6 },
  "is_abnormal": true
}
```

**Response `201`:**
```json
{
  "success": true,
  "data": {
    "record_id": "rec_a1b2c3d4",
    "patient_id": "pt_7f3a9b2c",
    "record_type": "LAB",
    "status": "RECEIVED"
  }
}
```

---

#### `POST /data/imaging` — Tıbbi Görüntü Yükle

**Yetki:** `ADMIN`, `DOCTOR`

**Content-Type:** `multipart/form-data`

**Form Alanları:**

| Alan | Tip | Açıklama |
|---|---|---|
| `patient_id` | string | Hasta kimliği |
| `modality` | string | MRI, CT, X-RAY, ULTRASOUND, PET |
| `body_part` | string | Görüntülenen bölge |
| `recorded_at` | datetime | Çekim tarihi |
| `file` | binary | DICOM veya JPEG/PNG dosyası |

**Dosya Limitleri:**
- DICOM: max 500 MB
- JPEG/PNG: max 50 MB
- İzin verilen formatlar: `.dcm`, `.jpg`, `.png`

**Response `202`:** (Dosya işleme kuyruğa alınır)
```json
{
  "success": true,
  "data": {
    "upload_id": "upl_x9y8z7",
    "status": "QUEUED",
    "estimated_processing_time_seconds": 120
  }
}
```

---

#### `POST /data/genetic` — Genetik Veri Yükle

**Yetki:** `ADMIN`, `DOCTOR`

**Request Body:**
```json
{
  "patient_id": "pt_7f3a9b2c",
  "panel_type": "FULL_GENOME | EXOME | SNP_PANEL | PHARMACOGENOMICS",
  "lab_reference": "string",
  "sequenced_at": "2026-03-01",
  "file_url": "string (güvenli iç depolama URL'i)",
  "checksum_sha256": "string"
}
```

---

#### `GET /data/{patient_id}/history` — Hasta Veri Geçmişi

**Yetki:** `ADMIN`, `DOCTOR`, `PATIENT`

**Query Parametreleri:**

| Parametre | Tip | Açıklama |
|---|---|---|
| `record_type` | string | Filtre: LAB, IMAGING, GENETIC vb. |
| `from_date` | date | Başlangıç tarihi |
| `to_date` | date | Bitiş tarihi |
| `page` | int | Sayfa numarası |

---

### 6.3 Analiz ve Modelleme

**Base path:** `/analysis`

#### `POST /analysis/statistical` — İstatistiksel Analiz Tetikle

**Yetki:** `ADMIN`, `ANALYST`, `DOCTOR`

**Request Body:**
```json
{
  "analysis_type": "DESCRIPTIVE | CORRELATION | REGRESSION | SURVIVAL",
  "dataset_scope": {
    "patient_ids": ["pt_7f3a9b2c"],
    "record_types": ["LAB", "VITAL_SIGNS"],
    "date_range": {
      "from": "2025-01-01",
      "to": "2026-03-30"
    }
  },
  "parameters": {
    "target_variable": "HbA1c",
    "covariates": ["AGE", "BMI", "BLOOD_PRESSURE"]
  },
  "output_format": "JSON | CSV | REPORT_PDF"
}
```

**Response `202`:**
```json
{
  "success": true,
  "data": {
    "job_id": "job_ana_001",
    "status": "QUEUED",
    "estimated_duration_seconds": 300
  }
}
```

---

#### `GET /analysis/jobs/{job_id}` — Analiz İş Durumu Sorgula

**Yetki:** `ADMIN`, `ANALYST`, `DOCTOR`

**Response `200`:**
```json
{
  "success": true,
  "data": {
    "job_id": "job_ana_001",
    "status": "RUNNING | COMPLETED | FAILED",
    "progress_percent": 65,
    "started_at": "2026-03-30T10:05:00Z",
    "completed_at": null,
    "result_url": null
  }
}
```

---

#### `GET /analysis/results/{job_id}` — Analiz Sonuçlarını Getir

**Yetki:** `ADMIN`, `ANALYST`, `DOCTOR`

> Yalnızca `status: COMPLETED` olan işler için kullanılabilir.

**Response `200`:**
```json
{
  "success": true,
  "data": {
    "job_id": "job_ana_001",
    "analysis_type": "CORRELATION",
    "summary": {
      "variables_analyzed": 4,
      "significant_correlations": 2
    },
    "results": { ... },
    "generated_at": "2026-03-30T10:10:00Z"
  }
}
```

---

#### `GET /analysis/models` — Mevcut Modelleri Listele

**Yetki:** Tüm roller

**Response `200`:**
```json
{
  "success": true,
  "data": [
    {
      "model_id": "mdl_diabetes_v2",
      "name": "Diyabet Risk Modeli",
      "version": "2.1.0",
      "algorithm": "Random Forest",
      "accuracy": 0.923,
      "last_trained": "2026-02-15",
      "status": "ACTIVE"
    }
  ]
}
```

---

### 6.4 Risk Tahmini ve Öneri

**Base path:** `/prediction`

#### `POST /prediction/risk` — Hastalık Risk Tahmini

**Yetki:** `ADMIN`, `DOCTOR`

**Request Body:**
```json
{
  "patient_id": "pt_7f3a9b2c",
  "model_id": "mdl_diabetes_v2",
  "include_data_types": ["LAB", "GENETIC", "VITAL_SIGNS"],
  "prediction_horizon_months": 12
}
```

**Response `200`:**
```json
{
  "success": true,
  "data": {
    "prediction_id": "pred_00123",
    "patient_id": "pt_7f3a9b2c",
    "model_id": "mdl_diabetes_v2",
    "risk_score": 0.74,
    "risk_level": "HIGH",
    "confidence": 0.89,
    "contributing_factors": [
      { "factor": "HbA1c", "importance": 0.42, "direction": "POSITIVE" },
      { "factor": "BMI", "importance": 0.28, "direction": "POSITIVE" },
      { "factor": "PHYSICAL_ACTIVITY", "importance": 0.15, "direction": "NEGATIVE" }
    ],
    "predicted_at": "2026-03-30T10:15:00Z",
    "valid_until": "2026-04-30T10:15:00Z"
  }
}
```

> **risk_level:** `LOW` (0.0–0.3) | `MEDIUM` (0.3–0.6) | `HIGH` (0.6–0.8) | `CRITICAL` (0.8–1.0)

---

#### `POST /prediction/recommendations` — Kişiselleştirilmiş Öneri Oluştur

**Yetki:** `ADMIN`, `DOCTOR`

**Request Body:**
```json
{
  "patient_id": "pt_7f3a9b2c",
  "prediction_id": "pred_00123",
  "recommendation_types": ["LIFESTYLE", "MEDICATION", "SCREENING", "REFERRAL"]
}
```

**Response `200`:**
```json
{
  "success": true,
  "data": {
    "recommendation_id": "rec_xk91",
    "patient_id": "pt_7f3a9b2c",
    "recommendations": [
      {
        "type": "LIFESTYLE",
        "priority": "HIGH",
        "title": "Fiziksel Aktivite Artışı",
        "description": "Haftada en az 150 dakika orta yoğunlukta aerobik egzersiz önerilir.",
        "evidence_level": "A"
      },
      {
        "type": "SCREENING",
        "priority": "HIGH",
        "title": "3 Aylık HbA1c Takibi",
        "description": "Kan şekeri kontrolü için 3 ayda bir HbA1c testi yaptırılmalıdır.",
        "evidence_level": "A"
      }
    ],
    "generated_at": "2026-03-30T10:16:00Z",
    "disclaimer": "Bu öneriler karar destek amaçlıdır. Nihai karar hekime aittir."
  }
}
```

---

#### `GET /prediction/history/{patient_id}` — Tahmin Geçmişi

**Yetki:** `ADMIN`, `DOCTOR`, `PATIENT`

**Query Parametreleri:** `model_id`, `from_date`, `to_date`, `page`

---

### 6.5 Raporlama ve Görselleştirme

**Base path:** `/reports`

#### `POST /reports/generate` — Rapor Oluştur

**Yetki:** `ADMIN`, `DOCTOR`, `ANALYST`

**Request Body:**
```json
{
  "report_type": "PATIENT_SUMMARY | POPULATION_STATS | MODEL_PERFORMANCE | RISK_DASHBOARD",
  "scope": {
    "patient_id": "pt_7f3a9b2c",
    "date_range": {
      "from": "2025-01-01",
      "to": "2026-03-30"
    }
  },
  "format": "PDF | HTML | JSON",
  "include_sections": ["VITALS_TREND", "LAB_RESULTS", "RISK_SCORES", "RECOMMENDATIONS"]
}
```

**Response `202`:**
```json
{
  "success": true,
  "data": {
    "report_id": "rpt_z9x8",
    "status": "GENERATING",
    "estimated_ready_seconds": 60
  }
}
```

---

#### `GET /reports/{report_id}` — Rapor İndir

**Yetki:** `ADMIN`, `DOCTOR`, `ANALYST`, `PATIENT` (kendi raporları)

**Response `200`:**  
`Content-Type: application/pdf` veya `application/json`  
Rapor dosyası binary olarak döner.

---

#### `GET /reports/visualizations/{patient_id}` — Görselleştirme Verisi Getir

**Yetki:** `ADMIN`, `DOCTOR`, `PATIENT`

**Query Parametreleri:**

| Parametre | Tip | Açıklama |
|---|---|---|
| `chart_type` | string | TREND, RISK_GAUGE, LAB_HEATMAP, TIMELINE |
| `metric` | string | Görselleştirilecek metrik (ör: HbA1c) |
| `period` | string | 1M, 3M, 6M, 1Y, ALL |

**Response `200`:**
```json
{
  "success": true,
  "data": {
    "chart_type": "TREND",
    "metric": "HbA1c",
    "labels": ["Oca 2025", "Nis 2025", "Tem 2025", "Eki 2025", "Oca 2026"],
    "values": [6.8, 7.1, 7.4, 7.2, 7.0],
    "unit": "%",
    "reference_range": { "min": 4.0, "max": 5.6 }
  }
}
```

---

## 7. Veri Güvenliği ve Gizlilik

### 7.1 Genel İlkeler

- Tüm API iletişimi **TLS 1.3** üzerinden yapılır.
- Kişisel Sağlık Bilgisi (PHI) yanıtlarda **maskelenir** (ör: ad, kimlik numarası görünmez).
- Tüm erişimler **audit log**'a kaydedilir.
- Veriler **AES-256** ile şifrelenerek depolanır.

### 7.2 Yasal Uyum

| Kural | Açıklama |
|---|---|
| **KVKK** (6698 sayılı Kanun) | Türkiye kişisel veri koruma mevzuatı |
| **HIPAA** | Uluslararası sağlık verisi gizlilik standardı |
| **HL7 FHIR R4** | Sağlık verisi değişim standardı (hedef uyum) |

### 7.3 Veri Minimizasyonu

- API yanıtları yalnızca talep edilen alanları döner.
- Hassas alanlar (`national_id`, iletişim bilgileri) asla ham olarak API'ye gönderilmez.
- Analiz endpoint'leri anonim/pseudonim veriyle çalışır.

### 7.4 Erişim Logları

Her API isteğinde şu bilgiler loglanır:

```
timestamp | user_id | role | endpoint | method | patient_id | ip_address | status_code | duration_ms
```

Loglar 5 yıl süreyle saklanır ve yalnızca yetkili personel tarafından incelenebilir.

---

## 8. Rate Limiting

| Rol | Limit |
|---|---|
| `ADMIN` | 1000 istek / dakika |
| `DOCTOR` | 300 istek / dakika |
| `ANALYST` | 200 istek / dakika |
| `PATIENT` | 60 istek / dakika |

Limit aşıldığında `429 Too Many Requests` döner. Response header'larında:

```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1743332400
```

---

## 9. Versiyonlama Stratejisi

- Versiyon bilgisi URL'e eklenir: `/v1/`, `/v2/`
- Yeni minör değişiklikler (alan ekleme) **geriye uyumlu** yapılır.
- Breaking change'ler yeni majör versiyon açar.
- Eski versiyon, yeni versiyonun yayınından **6 ay** sonra kullanımdan kaldırılır.
- Deprecation bildirimleri Response header'da iletilir:

```
Deprecation: true
Sunset: Mon, 30 Sep 2026 00:00:00 GMT
```

---

## 10. Açık Sorular ve Kararlar

Aşağıdaki konular ekip içinde netleştirilmeyi beklemektedir:

| # | Konu | Seçenekler | Durum |
|---|---|---|---|
| 1 | Backend teknoloji seçimi | FastAPI (Python) vs R Plumber vs Node.js | ❓ Karar bekleniyor |
| 2 | NoSQL veritabanı tercihi | MongoDB vs Cassandra vs HBase | ❓ Karar bekleniyor |
| 3 | Asenkron iş kuyruğu | Celery/Redis vs Kafka vs Spark Streaming | ❓ Karar bekleniyor |
| 4 | Görüntü işleme pipeline | DICOM sunucu entegrasyonu detayları | ❓ Karar bekleniyor |
| 5 | HL7 FHIR uyumu zorunlu mu? | Tam FHIR vs kısmi uyum | ❓ Karar bekleniyor |
| 6 | Genetik veri depolama | Onsite vs cloud (KVKK kısıtları) | ❓ Karar bekleniyor |

---


