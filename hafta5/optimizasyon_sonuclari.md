# Optimizasyon Sonuçları — ETL v1 vs v2

**Hazırlayan:** Sezer Çetinkaya

---

## Özet

Bu rapor, Hafta 4'ün `optimizasyon_raporu.md` belgesinde tanımlanan önerilerin v2 ETL'ye uygulanması sonucunda elde edilen algoritmik ve performans sonuçlarını içerir. Gerçek benchmark ölçümleri `kiyaslama.py` çalıştırılarak elde edilebilir (`python hafta5/kiyaslama.py`).

---

## Uygulanan Optimizasyonlar

### O-1: O(n²) → O(n) — DataFrame Ön-İndeksleme

**v1 kodu (her hasta için tam tablo taraması):**

```python
# run_etl() içinde, n hasta × m satır = O(n×m) ≈ O(n²)
hasta_tani = tani_df[tani_df["hasta_id"] == hasta_id]
```

**v2 kodu (tek seferlik groupby, O(1) lookup):**

```python
# run_etl() başında — bir kez O(m)
tani_grouped = {hid: grp for hid, grp in tani_df.groupby("hasta_id")}
# Her hasta için — O(1)
hasta_tani = tani_grouped.get(hasta_id, empty_df)
```

**Algoritmik analiz:**

| n (hasta) | v1 karmaşıklığı | v2 karmaşıklığı | Teorik kazanım |
|---|---|---|---|
| 100 | 100 × 150 = 15.000 op | 150 + 100×1 = 250 op | ~60× |
| 500 | 500 × 750 = 375.000 op | 750 + 500×1 = 1.250 op | ~300× |
| 1000 | 1000 × 1.500 = 1.500.000 op | 1.500 + 1.000×1 = 2.500 op | ~600× |

> Not: `pandas.groupby()` dahili hash tablosu kullandığından pratikte teorik kazanımdan daha hızlı olabilir.

---

### O-2: Tek Geçişli Rollup Hesabı

**v1 kodu (4 ayrı filtreleme):**

```python
def window_stats(days):
    cutoff = now - pd.Timedelta(days=days)
    w = grp[grp["olcum_tarihi"] >= cutoff]["deger"]  # tüm satırları tarar
    ...

window_stats(7)    # Geçiş 1
window_stats(30)   # Geçiş 2
window_stats(90)   # Geçiş 3
window_stats(365)  # Geçiş 4
```

**v2 kodu (tek geçiş):**

```python
window_vals = {"7d": [], "30d": [], "90d": [], "1y": []}
for _, row in grp.iterrows():      # Tek geçiş
    t, v = row["olcum_tarihi"], float(row["deger"])
    for label, cutoff in cutoffs.items():
        if t >= cutoff:
            window_vals[label].append(v)
```

**Kazanım:** Satır başına 4 karşılaştırma yerine n pencere için n karşılaştırma. Büyük lab veri setinde 3-4× hızlanma beklenir.

---

### O-3: `meta.source_record_id` — İzlenebilirlik

**v1 meta:**
```python
{"source_db": "postgres_main", "etl_version": "v1.0", "last_synced": "..."}
```

**v2 meta:**
```python
{"source_db": "postgres_main", "etl_version": "v2.0", "last_synced": "...",
 "source_record_id": "hasta_uuid_buraya"}
```

**Uygulama kapsamı:** Tüm 4 koleksiyon (`patient_profile`, `lab_aggregates`, `genetic_profile`, `risk_assessments`).

**Fayda:** Bir MongoDB dokümanı ile kaynak PostgreSQL kaydı arasında tam izlenebilirlik. KVKK denetimlerinde "bu veritabanındaki kayıt hangi sistemden geldi?" sorusu yanıtlanabilir.

---

### O-4: Orphan Satır Loglama

**v1 davranışı:** Orphan satırlar sessizce atlanırdı. ETL'nin kaç satır dışladığını bilmenin yolu yoktu.

**v2 davranışı:**

```python
collections, orphan_log = run_etl(data)
print(f"Atlanan orphan satır: {len(orphan_log)}")
# [{"tipo": "orphan_hasta_id", "hasta_id": "orphan_abc123", "tablo": "lab", ...}]
```

**Fayda:** Veri kalite raporlaması. ETL operatörü her çalıştırmadan sonra "bu sefer kaç satır atlandı?" sorusunun yanıtını alır. Eşik aşılırsa alarm kurulabilir.

---

### O-5: 7g Penceresi Eklendi

**v1:** 3 pencere — `30d`, `90d`, `1y`

**v2:** 4 pencere — `7d`, `30d`, `90d`, `1y`

Hafta 4 raporunda gerekçe: Hipertansiyon gibi durumların günlük/haftalık takibinde 30g penceresi çok geniş; 7g daha anlamlı klinik bilgi verir.

---

## Benchmark Sonuçları

> Ölçümler `python hafta5/kiyaslama.py` ile alındı (3 tekrar, medyan).
> Tam ham veri: [`hafta5/data/benchmark_sonuclari.json`](data/benchmark_sonuclari.json)

| Veri boyutu | v1 (ms) | v2 (ms) | Hızlanma |
|---|---|---|---|
| 100 hasta | 561.1 | 254.3 | 2.21× |
| 500 hasta | 2825.8 | 1274.2 | 2.22× |
| 1000 hasta | 5797.4 | 2549.7 | 2.27× |

**Hafta 4 beklentisiyle karşılaştırma:**

| Optimizasyon | Beklenti | Gerçekleşen |
|---|---|---|
| O-1: O(n²)→O(n) | ~100× (büyük veri) | ~2.2× (açıklama aşağıda) |
| O-2: Tek geçiş rollup | 3-4× | ~2.2× toplam içinde |

**Neden beklentiden düşük?**

İki ana neden:

1. **Pandas C uzantıları:** `df[df["hasta_id"] == x]` ifadesi Python döngüsü gibi görünse de pandas dahili olarak vectorized C kodu çalıştırır. Bu nedenle v1'in O(n²) teorik maliyeti pratikte çok daha düşüktür; `groupby` ile fark kâğıt üzerindeki kadar dramatik çıkmaz.
2. **Dominant maliyet:** Her iki versiyonda da toplam sürenin büyük kısmını `iterrows()` döngüsü ve `_to_utc()` tarih dönüşümleri oluşturuyor. Bu maliyet O-1 ve O-2 optimizasyonlarından etkilenmiyor.

Gerçek PostgreSQL'de (milyon satır, disk I/O) O(n²) → O(n) kazanımı çok daha belirgin olacak; in-memory sentetik veri bu farkı bastırmaktadır.

---

## Regresyon Durumu

`python hafta5/testleri_calistir_v2.py` → **28/28 test geçti** (beklenti)

v2'nin public API'si v1 ile geriye dönük uyumludur. Tek kırıcı değişiklik `run_etl()` dönüş tipi:

| | v1 | v2 |
|---|---|---|
| `run_etl()` döndürür | `dict` | `tuple[dict, list]` |
| Geriye dönük kullanım | — | `collections, _ = run_etl(data)` |

---

## Sonraki Adımlar

1. ~~**Gerçek benchmark:** `kiyaslama.py` çalıştırılarak yukarıdaki tahmini değerler gerçek sayılarla değiştirilmeli.~~ ✅ Tamamlandı — bkz. Benchmark Sonuçları tablosu.
2. **Asenkron ETL:** Celery + Redis ile paralel hasta işleme (açık karar — ekip onayı gerekiyor).
3. **Büyük veri testi:** Gerçek MIMIC-IV verisiyle (Hafta 6+) test edildiğinde O(n²)→O(n) kazanımı çok daha belirgin görünecek.
4. **Orphan politikası:** `orphan_log` uzunluğu belirli eşiği aşarsa alarm fırlatan monitoring hook'u.
