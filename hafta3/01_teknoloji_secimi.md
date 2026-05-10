# 01 — Teknoloji Seçimi: NoSQL Veritabanı

## 1. Use Case Özeti

İstatistiksel analiz ve modelleme modülünün ihtiyacı:

- **Heterojen hasta dokümanları:** Her hastanın test paneli, genetik analizi ve tıbbi geçmişi farklı yapıda olabilir. Kimisinde MR var, kimisinde yok; kimisinde tam genom dizilimi var, kimisinde sadece SNP paneli.
- **Okuma ağırlıklı erişim:** Risk skorlama, kohort analizi ve dashboard sorguları (Melek'in `/analysis`, `/prediction`, `/reports` endpoint'leri) büyük çoğunlukla read-only.
- **Karmaşık analitik sorgular:** "Yaşı 50+ olan, HbA1c > 7.0 ve `BRCA1` patojenik varyantı taşıyan hastaları getir" gibi çok kriterli, çok koleksiyonlu sorgular.
- **Pre-aggregated metrikler:** Doktor dashboard'ında 30 günlük ortalama tansiyon, son HbA1c değeri, son risk skoru gibi rollup'lar saniyeler içinde dönmeli (Hafta 1 paydaş analizinde belirlenen ≤5 sn hedefi).
- **Esnek şema evrimi:** Yeni model versiyonları yeni feature alanları getirecek. Şema migration'a girmeden alan eklenebilmeli.

## 2. Aday Teknolojiler

| Aday | Tip | Kısa açıklama |
|---|---|---|
| MongoDB | Doküman (BSON) | Esnek doküman, Aggregation Pipeline, JSON Schema validasyonu |
| Apache Cassandra | Wide-column | Yüksek yazma yükü, dağıtık, query-first tasarım |
| CouchDB | Doküman | MongoDB benzeri ama daha küçük ekosistem |
| Amazon DynamoDB | Anahtar-değer / doküman | Yönetilen, ölçeklenebilir ama vendor lock-in |

## 3. MongoDB vs Cassandra Karşılaştırması

| Kriter | MongoDB | Cassandra | Kazanan |
|---|---|---|---|
| **Veri yapısı** | Doküman (JSON/BSON), iç içe yapı, dizi | Wide-column, key-value benzeri | MongoDB ✅ (heterojen sağlık verisi için) |
| **Esnek şema** | Tam — alan ekleme migrasyonsuz | CQL şeması katı, ALTER TABLE gerekir | MongoDB ✅ |
| **Sorgu dili** | Aggregation Pipeline güçlü ($lookup, $facet, $unwind) | CQL — JOIN yok, ad-hoc sorgu sınırlı | MongoDB ✅ |
| **Yazma yükü** | İyi (10-50K writes/sec) | Çok yüksek (100K+ writes/sec) | Cassandra |
| **Time-series / sensor** | Time Series Collection eklenmiş ama orta seviye | Çok güçlü, native partition by time | Cassandra |
| **Validasyon** | `$jsonSchema` validator yerleşik | Yok, uygulama katmanında | MongoDB ✅ |

**Skor:** MongoDB 4 / Cassandra 2

## 4. Karar: MongoDB

### Gerekçeler

1. **Sorgu paterni uyumu.** Modülün koşturacağı analitik sorgular ad-hoc, çok kriterli ve agregasyon-yoğun. Aggregation Pipeline (`$match → $group → $facet`) Cassandra'nın query-first paradigmasıyla uyumsuz; Cassandra'da her yeni sorgu için yeni tablo tasarlamak gerekir.

2. **Heterojen sağlık verisi.** Bir hastanın `genetic_profile` dokümanı 100 varyant içerirken bir başkasınınki 10.000 olabilir. MongoDB doküman yapısı bunu doğal kapsar; Cassandra'da değişken uzunluklu kompozit yapılar için collection tipleri dolaylı çözüm sağlar ve sorgulanabilirlik düşer.

3. **Validasyon ve veri kalitesi.** `$jsonSchema` ile ICD-10 kodu, kan grubu enum'u, yaş aralığı gibi kısıtları **veritabanı seviyesinde** zorlayabiliriz. Sağlık verisinde bu kritik. Cassandra'da bu kısıtlar uygulama kodunda kaybolur ve unutulur.

4. **Aggregation Pipeline ↔ Melek'in API'si bire bir.** Melek'in `POST /analysis/statistical` endpoint'i `analysis_type: CORRELATION | REGRESSION | DESCRIPTIVE` parametreleri alıyor. Bunların her biri MongoDB'de tek bir aggregation pipeline'a karşılık geliyor — ekstra bir analitik motor (Spark) çağırmaya gerek kalmadan basit istatistikler için doğrudan MongoDB yeter. Spark sadece büyük ölçek için devreye girer.

### Cassandra'nın haklı olduğu tek senaryo

Eğer projede **sürekli akış halinde DICOM görüntü metadata'sı veya vital bulgu sensör verisi** olsaydı (saniyede binlerce yazma), Cassandra mantıklı olurdu. Mevcut tasarımda DICOM HDFS'te saklanıyor, vital bulgular klinik kayıt olarak günde birkaç kez giriliyor — yazma yükü sınırlı.

## 5. Diğer Adaylar — Reddedilme Gerekçeleri

- **CouchDB:** MongoDB'nin sunduklarını sunuyor ama ekosistemi küçük. PyMongo gibi olgun sürücüler yok; eğitim ve istihdam riski.
- **Amazon DynamoDB:** Yönetilen olması cazip ama (a) KVKK kapsamında veri yerleşimi yönetimi zor, (b) AWS vendor lock-in projenin uzun vadeli açık kaynak yaklaşımına aykırı, (c) ad-hoc analitik sorgu için tasarlanmamış.
- **PostgreSQL JSONB:** Akın'ın PostgreSQL kararı zaten OLTP için. Aynı veritabanını analitik için de kullanmak; (a) OLTP iş yükünü etkiler, (b) JSONB indeksleri MongoDB'nin doküman indekslerinin esnekliğine ulaşamaz.

## 6. Versiyon ve Deployment Notları

- **Hedef MongoDB versiyonu:** 7.0+ (Time Series Collection ve `$jsonSchema` v6 desteği için)
- **Deployment:** Hafta 3 kapsamında karar dışında — DevOps Hafta 4+ alacak (Atlas vs on-prem). Açık karar olarak listede.
- **Replica set / sharding:** Bu görevin kapsamında değil. Tasarım tek-node geliştirme ortamı varsayar; ölçeklenme planı sonraki sprintlerde.
