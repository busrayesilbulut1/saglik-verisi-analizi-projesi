# Optimizasyon Raporu — ETL Katmanı

**Hazırlayan:** Sezer Çetinkaya

---

## Özet

Bu rapor, Hafta 4 test süitinin bulgularına dayanarak PostgreSQL → MongoDB ETL sürecindeki darboğazları, iyileştirme fırsatlarını ve önerilen çözümleri içermektedir. Her öneri, test sonuçlarından türetilmiştir.

---

## 1. ETL Performans Darboğazları

### 1.1 Rollup Hesaplamasının Batch İçinde Yapılması

**Tespit:** `compute_lab_aggregates()` her hasta için tüm lab satırlarını 4 farklı zaman penceresi için yeniden tarar (7g, 30g, 90g, 1y). 100 hasta × ortalama 3 parametre × 4 pencere = 1.200 iterasyon.

**Senaryo:** 10.000 hasta ve 20 parametre için bu ~800.000 iterasyona çıkar.

**Öneri:** Pencereleri tek geçişte hesapla:

```python
# Mevcut (yavaş): her pencere için ayrı filtreleme
window_stats(7)   # tüm satırları tarar
window_stats(30)  # tüm satırları yeniden tarar
window_stats(90)  # tüm satırları yeniden tarar

# Önerilen (hızlı): tarihe göre sırala, bir kez tara
df_sorted = grp.sort_values("olcum_tarihi")
# Tüm pencereleri tek geçişte doldur
```

**Tahmini kazanım:** Büyük veri setlerinde 3-4× hızlanma.

---

### 1.2 `transform_patient` İçinde Tekrar Eden DataFrame Filtreleme

**Tespit:** Her hasta için `tani_df[tani_df["hasta_id"] == hasta_id]` ve `risk_df[risk_df["hasta_id"] == hasta_id]` çağrısı yapılıyor. 100 hastada bu 200 tam tablo taraması demek.

**Öneri:** ETL başlamadan önce `groupby` ile indeksle:

```python
tani_by_hasta = dict(tuple(tani_df.groupby("hasta_id")))
risk_by_hasta = dict(tuple(risk_df.groupby("hasta_id")))

# Sonra O(1) lookup:
hasta_tani = tani_by_hasta.get(hasta_id, pd.DataFrame())
```

**Tahmini kazanım:** O(n²) → O(n) karmaşıklık; 10.000 hastada ~100× hızlanma.

---

## 2. Denormalizasyon Getirisi

### 2.1 Pre-aggregated Rollup'ların Değeri

**Tespit:** Test B-02, kaynak (hasta-parametre çifti sayısı) ile hedef (lab_aggregates dokümanı) arasındaki oranı doğruladı. Pre-aggregation doğru çalışıyor.

**Bulgu:** `patient_profile.rollups.last_hba1c` sayesinde doktor dashboard'unun ilk yüklenmesinde MongoDB'ye tek sorgu atılıyor; yoksa `lab_aggregates` koleksiyonuna JOIN gerekirdi (2 sorgu).

**Öneri:** Rollup penceresini genişlet — `avg_systolic_30d` yanına `avg_systolic_7d` ekle (hipertansif hasta takibinde haftalık trend daha anlamlı).

---

### 2.2 Hangi Rollup'lar Anlık Hesaplanmalı?

| Rollup | Güncellenme sıklığı | Öneri |
|---|---|---|
| `last_hba1c` | 3 ayda bir lab testi | Batch yeterli |
| `avg_systolic_30d` | Günlük ölçüm | Batch yeterli |
| `latest_risk_score` | Model yeniden çalıştığında | Trigger-based (risk hesaplandığında anında güncelle) |
| `has_genetic_profile` | Nadiren değişir | Batch yeterli |

---

## 3. Batch Pencere Önerisi

**Mevcut tasarım:** Günlük batch (gece 03:00).

**Test bulgusu:** 100 hastalık sentetik veri 0.5 sn'nin altında işleniyor. 10.000 hasta için tahmini süre ~50 sn (lineer ölçekleme varsayımıyla). 100.000 hasta için tahmini ~8 dk.

**Tablo kritikliğine göre önerilen sıklık:**

| Tablo / Koleksiyon | Kritiklik | Önerilen Sıklık |
|---|---|---|
| `risk_assessments` | Yüksek (karar destek) | Model çalıştığında anında |
| `lab_aggregates` | Orta | Günlük batch |
| `patient_profile` rollup | Orta | Günlük batch |
| `genetic_profile` | Düşük (nadiren değişir) | Haftalık batch |
| `feature_store` | Yüksek (ML girişi) | Günlük batch + 7 gün TTL |

---

## 4. Eksik FK / Orphan Satır Politikası

**Tespit (Test D-02):** Sentetik veride 2 orphan lab satırı kasıtlı olarak yerleştirildi. Test bu satırları başarıyla tespit etti.

**Bulgu:** ETL'nin mevcut davranışı orphan satırları **sessizce dışlamak**. Bu KVKK açısından güvenli ama izlenebilirlik açısından riskli.

**Önerilen politika:**

```
ETL politikası — orphan satırlar için:
1. Satırı MongoDB'ye YAZMA
2. Logla: { "tipo": "orphan_hasta", "hasta_id": "...", "tablo": "lab_test", "satir_no": 42 }
3. Günlük ETL raporuna ekle: "Atlanan orphan satır sayısı: N"
4. N > threshold (örn. %1) ise alarm gönder
```

**Uygulama:** `etl_donusturucu.py`'de `run_etl()` fonksiyonuna `orphan_log: list` parametresi eklenebilir.

---

## 5. Katman İzlenebilirliği — `meta.source_record_id`

**Tespit:** Mevcut ETL'de `meta.last_synced` ve `meta.etl_version` var ama hangi PostgreSQL satırından geldiği kaydedilmiyor.

**Örnek sorun:** Doktor "Bu risk skoru neden yüksek?" diye sorarsa, MongoDB dokümanından PostgreSQL'deki orijinal `risk_degerlendirme` kaydına geri gidilemiyor.

**Öneri:** Her ETL dokümanına `meta.source_record_id` ekle:

```python
meta = {
    "source_db": "postgres_main",
    "source_record_id": str(hasta_id),          # hasta tablosu PK
    "etl_version": ETL_VERSION,
    "last_synced": datetime.now(timezone.utc).isoformat(),
}
```

Karmaşık birleştirmelerde (lab_aggregates gibi):

```python
"meta": {
    "source_record_ids": list(grp["test_id"]),  # hangi lab_test satırlarından üretildi
    ...
}
```

**Fayda:** Veri kalite sorunlarında ve KVKK denetimlerinde tam izlenebilirlik. Test D-03'te bu yapı eksik FK tespiti için de kullanılabilecekti.

---

## Özet Tablo

| # | Öneri | Etki | Öncelik |
|---|---|---|---|
| 1 | Rollup hesaplamasını tek geçişe indir | 3-4× hız | Orta |
| 2 | DataFrame gruplamayı önceden yap | ~100× hız (büyük veri) | Yüksek |
| 3 | `avg_systolic_7d` rollup ekle | Klinik değer | Düşük |
| 4 | `risk_assessments` için trigger-based güncelleme | Veri güncelliği | Yüksek |
| 5 | Orphan satır loglama politikası | İzlenebilirlik | Orta |
| 6 | `meta.source_record_id` eklenmesi | İzlenebilirlik + KVKK | Yüksek |

---

*Bu rapor, `testleri_calistir.py` çıktısındaki test bulgularına dayanarak hazırlanmıştır. Gerçek MIMIC-IV/TCGA verisiyle benchmark Hafta 5+ kapsamında yapılacaktır.*
