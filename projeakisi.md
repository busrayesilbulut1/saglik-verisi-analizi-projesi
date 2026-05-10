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

**Sezer Çetinkaya**:

1. haftanın görev başlığı: Gereksinim Toplama ve Paydaş Analizi: Doktor, veri bilimci, yönetim ve hasta olmak üzere 4 paydaş grubunun beklenti ve öncelikleri analiz edildi; fonksiyonel gereksinimler (DICOM desteği, risk analizi, dashboard) ve teknik gereksinimler (KVKK uyumu, ≤5 sn hız hedefi, ölçeklenebilirlik) belirlendi.

# Sağlık Verisi Analizi ve Tahminleme Sistemi

Bu proje kapsamında; hasta kayıtlarını, tıbbi görüntüleri ve genetik verileri bir araya getirerek hastalık risklerini öngören bir büyük veri platformu geliştirmeyi hedefliyoruz.

## Teknik Yaklaşım ve Araçlar

Projenin büyük veri yükünü yönetmek için Apache Spark ve Hadoop ekosistemini temel altyapı olarak belirledik. Analitik tarafta R ve scikit-learn kütüphanelerini kullanırken, veri depolama ihtiyacı için NoSQL mimarisi üzerinden ilerlemeyi planlıyoruz.

---

## 1. Hafta: Gereksinim Toplama ve Paydaş Analizi

Projenin ilk aşamasında, sistemden kimlerin ne beklediğini ve teknik olarak neleri başarmamız gerektiğini netleştirmeye çalıştım. Bu maddeler, ilerleyen haftalarda yapacağımız veri işleme ve geliştirme süreçleri için birer yol gösterici niteliğindedir.

### Paydaş Analizi

| Paydaş | Beklenti | Öncelik |
| :--- | :--- | :--- |
| Doktorlar | Güvenilir tahmin skorları ve hızlıca göz atabileceği görsel raporlar. | Kritik |
| Veri Bilimciler | Modelleri eğitmek için temizlenmiş ve optimize edilmiş veri setleri. | Yüksek |
| Hastane Yönetimi | KVKK/HIPAA gibi veri gizliliği standartlarına tam uyum. | Yüksek |
| Hastalar | Kişisel verilerinin anonimliği ve doğru yönlendirme. | Orta |

### Sistemden Beklenen Özellikler

#### Fonksiyonel Beklentiler
* **Geniş Veri Desteği:** Sistem sadece metin değil, DICOM (tıbbi görüntü) ve genetik verileri de kabul edebilecek esneklikte olmalı.
* **Risk Analizi:** Mevcut veriler üzerinden istatistiksel modellerle hastalık riski üretilmeli.
* **Kullanıcı Paneli:** Analiz sonuçları, doktorların kullanımına uygun, sade bir dashboard üzerinden sunulmalı.

#### Teknik ve Performans Beklentileri
* **Güvenlik:** Sağlık verisiyle çalıştığımız için uçtan uca şifreleme ve yetkilendirme katmanları şart. (KVKK uyumu için kritik).
* **Ölçeklenebilirlik:** Veri hacmi arttığında Spark/Hadoop yapısının performans kaybını önlemesini bekliyoruz.
* **Hız Hedefi:** Kullanıcı deneyimi açısından hasta dashboard'u ve raporlama ekranlarının ≤5 saniyede yüklenmesini hedefliyoruz. DICOM görüntü analizi ve model inference gibi işlemler asenkron çalışacağından bu hedefin kapsamı dışındadır.


**Melek Şimşek**: Veri temizleme yöntemleri araştırması.
**Mehmet Boztepe**: Sağlık veri setleri araştırması.

---

## 2. Hafta

### Veri Görselleştirme Araçlarını Keşfetme ve Uygulama
Tableau, Power BI, Plotly/Dash, Matplotlib/Seaborn ve Grafana karşılaştırıldı; paydaş katmanına göre araç stratejisi belirlendi (doktor dashboard → Plotly Dash, analiz → Matplotlib, yönetim → Power BI); 6 sağlık odaklı görselleştirme tipi tanımlandı; prototip grafikler üretildi.

**Teslim paketi:** [hafta2/](hafta2/) klasörü
- [hafta2/arac_karsilastirmasi.md](hafta2/arac_karsilastirmasi.md) — 5 aracın karşılaştırması, katmana göre araç stratejisi ve 6 görselleştirme tipi
- [hafta2/gorsellestirmeler.py](hafta2/gorsellestirmeler.py) — Risk Gauge, Lab Trend, Lab Heatmap ve Patient Timeline grafiklerinin Plotly prototipi


---

## 3. Hafta
### İstatistiksel Analiz Modülü Veritabanı Şeması Tasarımı

Bu hafta atanan görev kapsamında, istatistiksel analiz ve modelleme modülünün ihtiyaç duyacağı verileri saklamak için bir NoSQL veritabanı şeması tasarladım. Akın'ın PostgreSQL tabanlı operasyonel şeması (OLTP) üzerine, okuma ve analiz odaklı ikinci bir katman (OLAP) konumlandırdım.

**Teknoloji kararı:** MongoDB 7.0+ (Cassandra yerine). Heterojen sağlık dokümanları, `$jsonSchema` validasyonu ve Aggregation Pipeline ile istatistiksel sorgular için MongoDB'nin model uyumu yüksek bulundu.

**Mimari özet:**

```
PostgreSQL (Akın — OLTP)  ──ETL günlük batch──▶  MongoDB (OLAP)
hasta, tibbi_kayit, lab_sonuc...                 patient_profile,
denetim_kaydi, hasta_onayi                       lab_aggregates,
                                                 risk_assessments...
```

Tasarım, 16 PostgreSQL tablosunu denormalize ederek 7 MongoDB koleksiyonuna indirir. Pre-aggregated rollup'lar (30g/90g/1y pencereler) sayesinde dashboard sorguları saniyenin altında yanıtlanabilir hale gelir. KVKK uyumu olarak `tc_kimlik_no`, `email`, `telefon`, `ad/soyad` gibi alanlar MongoDB katmanına hiç gelmez; doğum tarihi yıla indirgenir; doktor ID'si SHA-256 ile pseudonimleştirilir.

**Tasarlanan 7 koleksiyon:**

| Koleksiyon | Amaç |
|---|---|
| `patient_profile` | Hasta özeti + rollup'lar (dashboard ilk yükleme) |
| `clinical_timeline` | Hasta kronolojik olay listesi |
| `lab_aggregates` | Pre-aggregated lab metrikleri |
| `genetic_profile` | Klinik öneme sahip varyantlar (ham VCF HDFS'te) |
| `imaging_metadata` | DICOM metadata + radyolog raporu |
| `risk_assessments` | ML model çıktıları + öneriler (zaman serisi) |
| `feature_store` | ML için hazır feature vektörleri (TTL: 7 gün) |

Şema, Melek'in API tasarımındaki `/analysis`, `/prediction` ve `/reports` endpoint'lerinin tüm veri ihtiyacını karşılayacak şekilde planlandı. Özellikle `GET /reports/visualizations/{patient_id}` endpoint'inin `chart_type=TREND | RISK_GAUGE | LAB_HEATMAP | TIMELINE` parametreleri sırasıyla `lab_aggregates`, `risk_assessments`, `lab_aggregates`, `clinical_timeline` koleksiyonları üzerinden beslenir.

**Teslim paketi:** [hafta3/](hafta3/) klasörü
- [hafta3/README.md](hafta3/README.md) — paket girişi ve okuma sırası
- [hafta3/01_teknoloji_secimi.md](hafta3/01_teknoloji_secimi.md) — MongoDB vs Cassandra karar belgesi
- [hafta3/02_etl_eslestirmesi.md](hafta3/02_etl_eslestirmesi.md) — Akın'ın PostgreSQL şemasından mapping
- [hafta3/03_sema_tasarimi.md](hafta3/03_sema_tasarimi.md) — 7 koleksiyonun doküman yapıları
- [hafta3/04_dogrulama_kurallari.js](hafta3/04_dogrulama_kurallari.js) — `$jsonSchema` validator scriptleri
- [hafta3/05_indeksler.js](hafta3/05_indeksler.js) — sorgu kalıbına uygun indeksler
- [hafta3/06_ornek_belgeler.json](hafta3/06_ornek_belgeler.json) — her koleksiyon için sentetik örnek dokümanlar
- [hafta3/07_sorgu_ornekleri.js](hafta3/07_sorgu_ornekleri.js) — 8 aggregation pipeline örneği
- [hafta3/08_api_entegrasyon_haritasi.md](hafta3/08_api_entegrasyon_haritasi.md) — Melek'in REST endpoint'lerinin hangi MongoDB koleksiyonundan beslendiğini gösteren harita

---

## 4. Hafta — Veri Dönüşümü ve Entegrasyon Testleri

Bu hafta Hafta 3'te tasarlanan PostgreSQL → MongoDB ETL katmanını test ettim. Mehmet'in test süitinin (CSV → temiz DataFrame) tamamladığı yerden devam ederek ETL dönüşüm ve çok kaynaklı birleştirme mantığını kapsayan 28 test yazdım.

**Test katmanları:**

| Katman | Test sayısı | Kapsam |
|---|---|---|
| A — Şema/Alan/KVKK | 10 | patient_id format, PII yasağı, enum kontrolü, ICD-10 regex |
| B — Sayım/Bütünlük | 8 | Satır sayısı, null oranı, float toleransı, tekrarsız ID |
| C — Dönüşüm Doğruluğu | 5 | Rollup hesaplamaları, aktif tanı filtresi, pathogenic count |
| D — Entegrasyon | 5 | Kartezyen çarpım yok, orphan tespiti, FK kontrolü, UTC normalize |

Testler gerçek veritabanı bağlantısı gerektirmez — Akın'ın 16 tablolu şemasını temsil eden sentetik PostgreSQL çıktısı üzerinde çalışır. Çalıştırma: `python hafta4/testleri_calistir.py`

Optimizasyon analizi 6 öneri sundu; öncelikli olanlar: DataFrame gruplamayı ETL başında yaparak O(n²) → O(n) karmaşıklık, `meta.source_record_id` ile tam izlenebilirlik, `risk_assessments` için trigger-based güncelleme.

**Teslim paketi:** [hafta4/](hafta4/) klasörü
- [hafta4/README.md](hafta4/README.md) — paket girişi ve hızlı başlangıç
- [hafta4/sentetik_veri.py](hafta4/sentetik_veri.py) — sentetik PostgreSQL çıktısı üreticisi
- [hafta4/etl_donusturucu.py](hafta4/etl_donusturucu.py) — test edilen ETL dönüşüm fonksiyonları
- [hafta4/test_sema.py](hafta4/test_sema.py) — Katman A testleri (10 test)
- [hafta4/test_mutabakat.py](hafta4/test_mutabakat.py) — Katman B testleri (8 test)
- [hafta4/test_entegrasyon.py](hafta4/test_entegrasyon.py) — Katman C+D testleri (10 test)
- [hafta4/testleri_calistir.py](hafta4/testleri_calistir.py) — ana runner (Mehmet stiliyle uyumlu)
- [hafta4/optimizasyon_raporu.md](hafta4/optimizasyon_raporu.md) — test bulgularına dayalı 6 optimizasyon önerisi

**Sprint toplantısı için açık soru:** İstatistiksel analiz modülünün NoSQL deposu olarak MongoDB lehine oylama önerisi sunulmuştur. Karar bu pakette gerekçelendirilmiş ve oylamaya hazır hale getirilmiştir.

---

## 5. Hafta — Veri Dönüşüm Optimizasyonu

Hafta 4'ün `optimizasyon_raporu.md` belgesindeki 5 öneriyi `etl_donusturucu_v2.py`'ye uygulayarak kodla kanıtladım. v1 referans olarak korundu.

**Uygulanan optimizasyonlar:**

| Kod | Açıklama | Etki |
|---|---|---|
| O-1 | `run_etl()` DataFrame filtreleme → groupby ile O(1) lookup | O(n²) → O(n) |
| O-2 | Rollup pencereleri 4 geçiş → tek geçiş | ~3× hız |
| O-3 | `meta.source_record_id` — kaynak PostgreSQL kaydı izlenebilir | KVKK denetim desteği |
| O-4 | Orphan satırlar loglanıyor (sessiz drop yerine `orphan_log` listesi) | Veri kalite raporlaması |
| O-5 | 7g rollup penceresi eklendi (`windows.7d`) | Hipertansiyon günlük takibi |

**v1'den tek API değişikliği:**
```python
collections, orphan_log = run_etl(data)   # v2
```

**Regresyon:** `python hafta5/testleri_calistir_v2.py` → Hafta 4'ün 28 testi v2 üzerinde geçiyor.

**Kıyaslama:** `python hafta5/kiyaslama.py` → 1000 hasta ölçeğinde v2, v1'den ~16× hızlı (sentetik veri; gerçek PostgreSQL'de çok daha fazla).

**Teslim paketi:** [hafta5/](hafta5/) klasörü
- [hafta5/etl_donusturucu_v2.py](hafta5/etl_donusturucu_v2.py) — 5 optimizasyon uygulanmış ETL
- [hafta5/kiyaslama.py](hafta5/kiyaslama.py) — v1 vs v2 zamanlama karşılaştırması
- [hafta5/testleri_calistir_v2.py](hafta5/testleri_calistir_v2.py) — Hafta 4 28 testini v2 üzerinde koşar
- [hafta5/optimizasyon_sonuclari.md](hafta5/optimizasyon_sonuclari.md) — algoritmik analiz + kıyaslama sonuçları
- [hafta5/README.md](hafta5/README.md) — paket girişi
