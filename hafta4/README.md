# Hafta 4 — Veri Dönüşümü ve Entegrasyon Testleri

**Hazırlayan:** Sezer Çetinkaya 

---

## Görev

> "Farklı veri kaynaklarından alınan verilerin birleştirilmesi ve dönüştürülmesi sürecini test et. Veri kaybı veya bozulma olup olmadığını kontrol et. Entegrasyon sürecini daha verimli hale getirmek için optimizasyon önerileri sun."

## Bu Paket Ne Yapar?

Akın'ın PostgreSQL şemasından (Akın/projeakisi.md) Sezer'in MongoDB şemasına ([hafta3/](../hafta3/)) akan ETL katmanını test eder.

**Mehmet'in testlerinden fark:** Mehmet CSV → temiz DataFrame katmanını test etti. Bu paket **PostgreSQL → MongoDB dönüşüm ve birleştirme** katmanını test eder — farklı, tamamlayıcı.

## Hızlı Başlangıç

```bash
# Bağımlılıklar
pip install pandas numpy

# Çalıştır
python hafta4/testleri_calistir.py
```

Çıktı:

```
=================================================================
  BAYT BÜKÜCÜLER — HAFTA 4 ETL & ENTEGRASYON TEST SÜİTİ
=================================================================

  📦 Sentetik PostgreSQL verisi üretiliyor...
     ✓ hasta     :  100 satır
     ✓ lab       :  300 satır
     ...

─────────────────────────────────────────────────────────────────
  KATMAN A — ŞEMA / ALAN / KVKK TESTLERİ
─────────────────────────────────────────────────────────────────
  patient_id Format                              ✅  100 profil kontrol edildi
  PII Alan Yasağı (tc_kimlik_no, ad ...)         ✅  Hiçbir PII alanı bulunamadı
  ...

  TOPLAM: 28 test | GEÇTİ: 26 | ATLANDI: 2 | BAŞARISIZ: 0
  ✅ 26/28 test geçti — 2 atlandı (normal)
=================================================================
```

JSON rapor: `hafta4/data/test_raporu_hafta4.json`

## Dosya Yapısı

```
hafta4/
├── README.md                 ← bu dosya
├── sentetik_veri.py          ← Sentetik PostgreSQL çıktısı üreticisi
├── etl_donusturucu.py        ← Test edilen ETL dönüşüm fonksiyonları
├── test_sema.py              ← Katman A: alan/tip/KVKK testleri (10 test)
├── test_mutabakat.py         ← Katman B: sayım/bütünlük testleri (8 test)
├── test_entegrasyon.py       ← Katman C+D: dönüşüm + entegrasyon (10 test)
├── testleri_calistir.py      ← Ana runner
├── optimizasyon_raporu.md    ← Test bulgularına dayalı öneriler
└── data/                     ← testleri_calistir.py tarafından oluşturulur
    └── test_raporu_hafta4.json
```

## Test Katmanları (28 Test)

| Katman | Dosya | Test sayısı | Kapsam |
|---|---|---|---|
| **A** | test_sema.py | 10 | patient_id format, PII yasağı, enum, ICD-10 regex |
| **B** | test_mutabakat.py | 8 | Satır sayısı, null oranı, float toleransı, tekrarsız ID |
| **C** | test_entegrasyon.py (ilk 5) | 5 | Rollup doğruluğu, aktif tanı filtresi, pathogenic count |
| **D** | test_entegrasyon.py (son 5) | 5 | Kartezyen çarpım yok, orphan tespiti, FK kontrolü, UTC |

## Diğer Ekip Üyeleriyle İlişki

| Ekip üyesi | Çalışma | Bu paketle bağlantı |
|---|---|---|
| **Akın** | 16 tablolu PostgreSQL şeması | ETL'nin **kaynağı** — sentetik_veri.py bu şemayı simüle eder |
| **Mehmet** | CSV → temiz DataFrame pipeline + testleri | Bu paket Mehmet'in çıktısından **sonraki katmanı** test eder |
| **Melek** | API tasarımı (/analysis, /prediction) | ETL çıktısının **tüketicisi** — doğru şema üretilmezse API bozulur |

## Optimizasyon Önerileri

Detaylar için [optimizasyon_raporu.md](optimizasyon_raporu.md). Özetle:

1. DataFrame gruplamayı ETL başında yap → O(n²) → O(n)
2. Rollup pencerelerini tek geçişte hesapla → 3-4× hız
3. `risk_assessments` için trigger-based güncelleme
4. Orphan satır loglama politikası
5. `meta.source_record_id` ile tam izlenebilirlik
