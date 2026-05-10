# Hafta 5 — Veri Dönüşüm Optimizasyonu

**Hazırlayan:** Sezer Çetinkaya 

---

## Görev

> "Hafta 4'te oluşturulan veri dönüşüm süreçlerini analiz et ve optimizasyon fırsatlarını belirle. Daha hızlı ve etkili dönüşüm için algoritmaları ve yöntemleri geliştir."

## Bu Paket Ne Yapar?

Hafta 4'te `optimizasyon_raporu.md`'de belgelenen 6 öneriden 5'ini `etl_donusturucu_v2.py`'ye uygular ve kıyaslama ile kanıtlar.

## Hızlı Başlangıç

```bash
pip install pandas numpy   # v1 ile aynı bağımlılıklar

# Regresyon — 28 test v2 ETL üzerinde
python hafta5/testleri_calistir_v2.py

# Kıyaslama — v1 vs v2 zamanlama (100 / 500 / 1000 hasta)
python hafta5/kiyaslama.py
```

## Dosya Yapısı

```
hafta5/
├── README.md
├── etl_donusturucu_v2.py     ← 5 optimizasyon uygulanmış ETL
├── kiyaslama.py              ← v1 vs v2 zamanlama + regresyon özeti
├── testleri_calistir_v2.py   ← Hafta 4'ün 28 testini v2 ile koşar
└── optimizasyon_sonuclari.md ← Algoritmik analiz + kıyaslama sonuçları
```

## Uygulanan 5 Optimizasyon

| Kod | Açıklama | Etki |
|---|---|---|
| **O-1** | `run_etl()` DataFrame filtreleme → groupby ile O(1) lookup | O(n²) → O(n) |
| **O-2** | Rollup pencereleri 4 geçiş → tek geçiş | ~3× hız |
| **O-3** | `meta.source_record_id` eklendi | Tam izlenebilirlik |
| **O-4** | Orphan satırlar loglanıyor (sessiz drop yok) | Veri kalite raporlaması |
| **O-5** | 7g penceresi eklendi (`windows.7d`) | Klinik değer |

## v1'den Tek API Değişikliği

```python
# v1
collections = run_etl(data)

# v2
collections, orphan_log = run_etl(data)
# veya geriye dönük uyumlu:
collections, _ = run_etl(data)
```

## Bağlantılar

| Dosya | Açıklama |
|---|---|
| [hafta4/etl_donusturucu.py](../hafta4/etl_donusturucu.py) | v1 — referans olarak korunur |
| [hafta4/optimizasyon_raporu.md](../hafta4/optimizasyon_raporu.md) | Uyguladığımız 6 önerinin kaynağı |
| [hafta3/02_etl_eslestirmesi.md](../hafta3/02_etl_eslestirmesi.md) | ETL mantığının tasarım belgesi |
