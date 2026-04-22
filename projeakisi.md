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
## 📋 Hafta 1: Proje Analizi ve Kapsam Belirleme

### 1. Genel Hedefler ve Kapsam Analizi
Projenin temel amacı, modern tıpta "veri siloları" (birbirinden kopuk veri kümeleri) olarak adlandırılan yapıları birleştirerek, hastayı 360 derecelik bir bakış açısıyla analiz etmektir.

* **Bütünsel Teşhis:** Sadece tek bir veri tipine (örneğin sadece röntgen) bağlı kalmaksızın; genetik yatkınlık, klinik geçmiş ve radyolojik bulguları birleştiren **Multimodal (Çok Modlu) AI** mimarisi kurmak.
* **Erken Teşhis Mekanizması:** Hastalık belirtileri klinik olarak ortaya çıkmadan önce, genetik mutasyonlar ve mikro-radyolojik değişimler üzerinden yüksek doğruluklu risk tahminleri üretmek.
* **Kişiselleştirilmiş Tedavi (Precision Medicine):** "Her hastaya aynı tedavi" yaklaşımı yerine, hastanın biyolojik ve genetik profiline en uygun, yan etkisi en düşük tedavi protokollerini önermek.

### 2. Çalışılacak Veri Kümeleri (Data Clusters)
Proje, heterojen veri yapılarını işleyebilmek adına aşağıdaki standart ve açık kaynaklı veri setlerini temel almaktadır:

| Veri Kategorisi | Veri Seti Örneği | İçerik ve Teknik Rol |
| :--- | :--- | :--- |
| **Klinik Kayıtlar** | **MIMIC-IV** | Yapılandırılmış veriler; demografi, laboratuvar sonuçları, vital bulgular ve EHR (Elektronik Sağlık Kayıtları). |
| **Tıbbi Görüntüleme** | **TCIA / Kaggle** | Yapılandırılmamış veriler; BT (BT), MR ve röntgen formatındaki DICOM görüntüleri. |
| **Genetik Bilgiler** | **TCGA (The Cancer Genome Atlas)** | Karmaşık veriler; DNA/RNA dizilimleri, genetik mutasyonlar ve varyasyon tabloları. |
| **Tedavi Verileri** | **DrugBank / ClinVar** | Referans veriler; genetik varyasyonların ilaçlara verdiği tepkiler ve tedavi protokolleri. |

### 3. Elde Edilecek İçgörüler (Insights)
Sistemin analiz süreçleri sonucunda şu kritik çıktıların elde edilmesi hedeflenmektedir:

* **Dinamik Risk Skorlaması:** Hastanın mevcut klinik tablosu ile genetik risk faktörlerinin birleştirilerek "hastalık gelişim olasılığı" grafiğinin oluşturulması.
* **Fenotip-Genotip Korelasyonu:** Görüntüleme verilerindeki (fenotip) anomalilerin, hangi genetik mutasyonlarla (genotip) eşleştiğinin saptanması.
* **Farmakogenomik Tahminleme:** Hastanın genetik yapısına göre belirli ilaçların toksisite riskinin ve etkinlik oranının önceden belirlenmesi.
* **Klinik Karar Destek:** Doktorların teşhis sürecini hızlandırmak amacıyla karmaşık verilerin süzülerek anlamlı bir "ikinci görüş" paneline dönüştürülmesi.

---
**Hazırlayan:** Akın Ağaçbacak

**Sezer Çetinkaya**:
# Sağlık Verisi Analizi ve Tahminleme Sistemi

Bu proje kapsamında; hasta kayıtlarını, tıbbi görüntüleri ve genetik verileri bir araya getirerek hastalık risklerini öngören bir büyük veri platformu geliştirmeyi hedefliyoruz.

## Teknik Yaklaşım ve Araçlar

Projenin büyük veri yükünü yönetmek için Apache Spark ve Hadoop ekosistemini temel altyapı olarak belirledik. Analitik tarafta R ve scikit-learn kütüphanelerini kullanırken, veri depolama ihtiyacı için NoSQL mimarisi üzerinden ilerlemeyi planlıyoruz.

---

## 1. Hafta: Gereksinim Analizi ve Paydaş Beklentileri

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
* **Hız Hedefi:** Kullanıcı deneyimi açısından raporlama ve analiz süreçlerinin 5 saniye gibi makul sürelerde tamamlanmasını hedefliyoruz (Altyapı araştırmalarında bu süre baz alınabilir).

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
## 📊 Veri Kaynaklarına Erişim ve Veri Ön İşleme Sürecinin Planlanması

Bu proje kapsamında sorumluluğum, sistemde kullanılacak sağlık verilerine erişimi sağlamak ve bu verilerin analiz için uygun hale getirilmesini sağlayacak **veri ön işleme sürecini planlamaktır**. Sağlık alanında kullanılan veri setleri genellikle farklı kaynaklardan elde edilir ve çoğu zaman farklı formatlarda, eksik veya düzensiz bilgiler içerebilir. Bu nedenle veri analizi ve makine öğrenmesi modellerinin doğru sonuçlar üretebilmesi için verilerin dikkatli bir şekilde hazırlanması gerekmektedir.

---

### 📁 Veri Kaynaklarına Erişim

Projenin ilk aşamasında kullanılabilecek veri kaynaklarının belirlenmesi ve bu kaynaklara erişim sağlanması hedeflenmektedir. Sağlık verileri farklı türlerde olabilir ve bu projede özellikle aşağıdaki veri türleri üzerinde durulmaktadır:

- **Hasta kayıtları**
  - Hastaların yaş, cinsiyet, hastalık geçmişi ve laboratuvar sonuçları gibi klinik bilgileri içerir.

- **Tıbbi görüntüleme verileri**
  - Röntgen, MR veya tomografi gibi teşhis amaçlı kullanılan görüntü verileridir.

- **Genetik veriler**
  - Bireylerin genetik yapısına ait bilgiler ve hastalıklarla ilişkili genetik varyasyonları içerir.

Bu veri türleri açık veri platformları, akademik veri tabanları ve araştırma veri setlerinden elde edilerek proje veri altyapısına aktarılacaktır.

---

### 🧹 Veri Ön İşleme Süreci

Ham sağlık verileri doğrudan analiz için uygun değildir. Bu nedenle veri setlerinin analiz ve modelleme için hazırlanması amacıyla **veri ön işleme adımları** uygulanacaktır.

#### 1️⃣ Veri Temizleme

Bu aşamada veri setlerinde bulunan eksik, hatalı veya tutarsız bilgiler belirlenir ve düzeltilir.

Yapılacak işlemler:

- Eksik verilerin tespit edilmesi  
- Hatalı veya tutarsız verilerin düzeltilmesi  
- Tekrarlanan kayıtların kaldırılması  

Bu işlem veri setinin güvenilirliğini artırır.

---

#### 2️⃣ Veri Dönüştürme

Farklı veri kaynaklarından gelen veriler çoğu zaman farklı formatlarda olabilir. Bu nedenle verilerin analiz için uygun hale getirilmesi gerekir.

Bu süreçte:

- Veri formatları standart hale getirilir  
- Kategorik veriler sayısal verilere dönüştürülür  
- Veri ölçeklendirme işlemleri uygulanır  

Bu adım makine öğrenmesi algoritmalarının veriyi daha doğru kullanmasını sağlar.

---

#### 3️⃣ Veri Entegrasyonu

Projede birden fazla veri kaynağı kullanılacağı için bu verilerin bir araya getirilmesi gerekir. Hasta kayıtları, laboratuvar sonuçları ve diğer sağlık verileri birleştirilerek daha kapsamlı bir veri yapısı oluşturulur.

Bu sayede sistem her hasta için daha detaylı bir veri profiline sahip olur ve analizler daha doğru sonuçlar üretebilir.

---

### 🎯 Sürecin Proje İçindeki Önemi

Veri kaynaklarına erişim ve veri ön işleme süreci, projenin temelini oluşturmaktadır. Bu aşamada elde edilen temiz ve düzenli veri setleri, projenin sonraki aşamalarında gerçekleştirilecek olan:

- İstatistiksel analiz
- Makine öğrenmesi modelleri
- Hastalık risk tahmin sistemleri

için gerekli veri altyapısını sağlayacaktır. Doğru şekilde hazırlanmış veri setleri sistemin daha güvenilir ve doğru sonuçlar üretmesini mümkün kılacaktır.

---

## 2. Hafta
## 🎯 Hafta 2 Hedefleri
 
- Tekrar eden manuel temizleme işlemlerini **otomatik** hale getirmek
- Farklı veri kaynaklarında (MIMIC-IV, TCGA, DrugBank) çalışabilen **tek bir modüler pipeline** kurmak
- Eksik veri, aykırı değer ve veri dönüştürme adımlarını **standartlaştırmak**
- KVKK uyumu için **anonimleştirme** katmanı eklemek
- Her çalışmada karşılaştırılabilir **kalite raporu** üretmek
---
 
## 🗂️ Dosya Yapısı
 
```
bayt-bukuculer/
├── data/
│   ├── hasta_kayitlari.csv          # Ham veri (örnek)
│   └── hasta_kayitlari_temiz.csv    # Pipeline çıktısı
├── hafta2/
│   ├── data_cleaning_pipeline.py    # Ana pipeline modülü  ← bu hafta
│   ├── pipeline.log                 # Otomatik oluşturulan log
│   └── cleaning_report.json         # Otomatik oluşturulan rapor
└── README.md
```
 
---
 
## ⚙️ Pipeline Adımları
 
Aşağıdaki 10 adım, `run_pipeline()` fonksiyonu çağrıldığında sırayla ve otomatik olarak çalışır.
 
### 1. Veri Yükleme (`load_data`)
CSV ve JSON formatlarını destekler. Yüklenen veri boyutu log'a yazılır.
 
### 2. Ham Kalite Raporu (`generate_quality_report`)
Temizleme **öncesinde** bir fotoğraf çeker:
- Toplam satır / sütun sayısı
- Sütun bazında eksik değer oranı (%)
- Tekrarlanan satır sayısı
- Veri tipleri
### 3. Tekrarlanan Kayıt Kaldırma (`remove_duplicates`)
Aynı hasta kaydının birden fazla kez sisteme girilmesi gibi durumları önler. İsteğe bağlı olarak belirli sütunlar (`subset`) üzerinden kontrol edilebilir.
 
### 4. Eksik Değer İşleme (`handle_missing_values`)
 
| Veri Tipi | Strateji |
|-----------|----------|
| Sayısal | Medyan ile doldur |
| Kategorik | En sık değer (mod) ile doldur |
| Eksik oranı > %50 | Sütunu kaldır (`"drop"` stratejisinde) |
 
Hafta 1'deki manuel yaklaşımın aksine strateji artık parametre olarak dışarıdan verilmektedir; farklı veri setleri için ayrı kod yazılmasına gerek kalmaz.
 
### 5. Aykırı Değer Tespiti (`remove_outliers_iqr`)
IQR (Interquartile Range) yöntemi kullanılır:
 
```
Alt sınır = Q1 - 1.5 × IQR
Üst sınır = Q3 + 1.5 × IQR
```
 
> ⚠️ **Tıbbi Not:** Bazı aşırı değerler (örn. kritik kan basıncı) klinik anlam taşıyabilir. Bu nedenle `outlier_columns` listesi dikkatle belirlenmelidir.
 
### 6. Kategorik Kodlama (`encode_categoricals`)
`cinsiyet`, `kan_grubu`, `tani_kodu` gibi metin tabanlı sütunlar `LabelEncoder` ile sayısal değerlere dönüştürülür. Makine öğrenmesi modellerinin veriyi doğru işlemesi için zorunludur.
 
### 7. Normalizasyon (`normalize_numeric`)
Sayısal sütunlar Min-Max Scaling ile [0, 1] aralığına çekilir. Bu adım özellikle scikit-learn ve TensorFlow modellerinde öğrenme hızını ve doğruluğunu artırır.
 
### 8. KVKK Uyumlu Anonimleştirme (`anonymize_columns`)
`hasta_id`, `tc_kimlik_no`, `email` gibi doğrudan kimlik belirleyici sütunlar **SHA-256 hash** ile maskelenir. Bu adım:
- KVKK Madde 5-6 gerekliliklerini karşılar
- Üretim ortamında tokenizasyona geçiş için hazırlar
- Denetim izini (`denetim_kaydi` tablosu) bozmadan çalışır
### 9. Veri Doğrulama (`validate_data`)
Tanımlanmış kurallara aykırı veriler **kaldırılmadan** raporlanır. Örnek kurallar:
 
```python
validation_rules = {
    "yas":          {"min": 0, "max": 120},
    "cinsiyet":     {"allowed": ["E", "K", "Bilinmiyor"]},
    "sistolik_kb":  {"min": 60, "max": 250}
}
```
 
### 10. Rapor ve Kayıt (`save_report`)
`cleaning_report.json` içinde temizleme öncesi/sonrası karşılaştırma otomatik üretilir:
 
```json
{
  "özet": {
    "önceki_satır": 15000,
    "sonraki_satır": 14237,
    "kaldırılan_satır": 763,
    "önceki_eksik_sütun_sayısı": 8,
    "sonraki_eksik_sütun_sayısı": 0
  }
}
```
 
---
 
## 🚀 Kullanım
 
```bash
# Gerekli kütüphaneleri kur
pip install pandas numpy scikit-learn
 
# Pipeline'ı çalıştır
python hafta2/data_cleaning_pipeline.py
```
 
Farklı veri setleri için `run_pipeline()` çağrısını parametrelendirin:
 
```python
from data_cleaning_pipeline import run_pipeline
 
temiz_df = run_pipeline(
    input_path="data/hasta_kayitlari.csv",
    output_path="data/hasta_kayitlari_temiz.csv",
    outlier_columns=["yas", "sistolik_kb", "nabiz"],
    categorical_columns=["cinsiyet", "kan_grubu"],
    normalize_columns=["yas", "sistolik_kb"],
    sensitive_columns=["tc_kimlik_no", "email"],
    validation_rules={"yas": {"min": 0, "max": 120}},
    missing_strategy="auto"
)
```
 
---
 
## 🔄 Hafta 1'e Göre İyileştirmeler
 
| Konu | Hafta 1 (Manuel) | Hafta 2 (Otomatik Pipeline) |
|------|------------------|-----------------------------|
| Eksik değer doldurma | Sütun sütun, ayrı kod | Tip bazlı otomatik strateji |
| Tekrarlanan kayıt | Elle kontrol | `remove_duplicates()` |
| Aykırı değer | Tanımsız | IQR yöntemi, eşik ayarlanabilir |
| Kategorik dönüşüm | Ayrı script | Pipeline içinde entegre |
| Normalizasyon | Yok | Min-Max Scaler entegre |
| KVKK anonimleştirme | Yok | SHA-256 hash katmanı |
| Kalite raporu | Yok | JSON rapor otomatik üretilir |
| Loglama | Yok | `pipeline.log` otomatik oluşturulur |
 
---
## 3. Hafta
## Veritabanı Şeması Tasarımı

### Genel Bakış
 
Şema 16 tablodan oluşmakta olup 5 ana gruba ayrılır:
 
```
saglik_db/
├── 🔵 Klinik Çekirdek        → hasta, doktor, hastane, tibbi_kayit, tani
├── 🟢 Reçete Yönetimi        → ilac_recete, ilac_kalemi
├── 🟡 Medikal Görüntüleme    → tibbi_goruntu
├── 🟣 Laboratuvar            → lab_test, lab_sonuc
├── 🔴 Genetik Veriler        → genetik_profil, genetik_varyant
├── 🔷 ML / Risk Katmanı      → risk_degerlendirme, oneri
└── 🟤 Güvenlik & Uyumluluk   → hasta_onayi, denetim_kaydi
```
 
---
 
### Şema Diyagramı
 
> Renk kodlaması: 🔵 Klinik · 🟢 Reçete · 🟡 Görüntüleme · 🟣 Lab · 🔴 Genetik · 🔷 ML/Risk · 🟤 Güvenlik

 ```mermaid
erDiagram
  HASTA {
    uuid hasta_id PK
    string tc_kimlik_no UK
    string ad
    string soyad
    date dogum_tarihi
    string cinsiyet
    string kan_grubu
    string telefon
    string email
    timestamp olusturma_tarihi
  }
 
  DOKTOR {
    uuid doktor_id PK
    string ad
    string soyad
    string uzmanlik_alani
    string lisans_no UK
    uuid hastane_id FK
    string email
  }
 
  HASTANE {
    uuid hastane_id PK
    string ad
    string adres
    string sehir
    string telefon
    string akreditasyon_no
  }
 
  TIBBI_KAYIT {
    uuid kayit_id PK
    uuid hasta_id FK
    uuid doktor_id FK
    timestamp ziyaret_tarihi
    text sikayet
    text tani_notu
    text tedavi_notu
    string kayit_turu
  }
 
  TANI {
    uuid tani_id PK
    uuid kayit_id FK
    string icd10_kodu
    string tani_adi
    string siddet
    date tani_tarihi
    boolean aktif
  }
 
  ILAC_RECETE {
    uuid recete_id PK
    uuid kayit_id FK
    uuid hasta_id FK
    uuid doktor_id FK
    date recete_tarihi
    date gecerlilik_tarihi
    string durum
  }
 
  ILAC_KALEMI {
    uuid kalem_id PK
    uuid recete_id FK
    string ilac_adi
    string atc_kodu
    string dozaj
    string kullanim_sikli
    int sure_gun
    text talimatlar
  }
 
  TIBBI_GORUNTU {
    uuid goruntu_id PK
    uuid hasta_id FK
    uuid kayit_id FK
    string goruntu_turu
    string dicom_uid UK
    string depolama_yolu
    timestamp cekim_tarihi
    text radyolog_raporu
    string sifreleme_anahtari
  }
 
  LAB_TEST {
    uuid test_id PK
    uuid hasta_id FK
    uuid kayit_id FK
    string test_adi
    string loinc_kodu
    timestamp numune_tarihi
    timestamp sonuc_tarihi
    string durum
  }
 
  LAB_SONUC {
    uuid sonuc_id PK
    uuid test_id FK
    string parametre_adi
    float deger
    string birim
    float referans_min
    float referans_max
    string yorum
  }
 
  GENETIK_PROFIL {
    uuid profil_id PK
    uuid hasta_id FK
    string analiz_turu
    string platform
    date analiz_tarihi
    string depolama_yolu
    string sifreleme_anahtari
    text ozet
  }
 
  GENETIK_VARYANT {
    uuid varyant_id PK
    uuid profil_id FK
    string gen_adi
    string rsid
    string konum
    string allel
    string klinik_onemi
    float risk_skoru
  }
 
  RISK_DEGERLENDIRME {
    uuid degerlendirme_id PK
    uuid hasta_id FK
    string hastalik_adi
    float risk_skoru
    string risk_kategorisi
    timestamp hesaplama_tarihi
    string model_versiyonu
    text aciklama
  }
 
  ONERI {
    uuid oneri_id PK
    uuid hasta_id FK
    uuid degerlendirme_id FK
    string oneri_turu
    text icerik
    int oncelik
    timestamp olusturma_tarihi
    boolean gosterildi
  }
 
  HASTA_ONAYI {
    uuid onay_id PK
    uuid hasta_id FK
    string onay_turu
    boolean onay_verildi
    timestamp onay_tarihi
    string ip_adresi
    int versiyon
  }
 
  DENETIM_KAYDI {
    uuid log_id PK
    string tablo_adi
    uuid kayit_id
    string islem_turu
    uuid kullanici_id
    timestamp islem_tarihi
    text onceki_deger
    text yeni_deger
    string ip_adresi
  }
 
  HASTANE           ||--o{  DOKTOR              : "bünyesinde çalışır"
  HASTA             ||--o{  TIBBI_KAYIT         : "sahiptir"
  DOKTOR            ||--o{  TIBBI_KAYIT         : "yazar"
  TIBBI_KAYIT       ||--o{  TANI                : "içerir"
  TIBBI_KAYIT       ||--o{  ILAC_RECETE         : "oluşturur"
  HASTA             ||--o{  ILAC_RECETE         : "alır"
  DOKTOR            ||--o{  ILAC_RECETE         : "yazar"
  ILAC_RECETE       ||--o{  ILAC_KALEMI         : "içerir"
  HASTA             ||--o{  TIBBI_GORUNTU       : "sahiptir"
  TIBBI_KAYIT       ||--o{  TIBBI_GORUNTU       : "içerir"
  HASTA             ||--o{  LAB_TEST            : "yaptırır"
  TIBBI_KAYIT       ||--o{  LAB_TEST            : "içerir"
  LAB_TEST          ||--o{  LAB_SONUC           : "üretir"
  HASTA             ||--o|  GENETIK_PROFIL      : "sahiptir"
  GENETIK_PROFIL    ||--o{  GENETIK_VARYANT     : "içerir"
  HASTA             ||--o{  RISK_DEGERLENDIRME  : "değerlendirilir"
  RISK_DEGERLENDIRME||--o{  ONERI               : "üretir"
  HASTA             ||--o{  ONERI               : "alır"
  HASTA             ||--o{  HASTA_ONAYI         : "verir"
```
 
---
 
### Graphviz DOT Diyagramı
<img width="1701" height="2429" alt="graphviz" src="https://github.com/user-attachments/assets/dbccb12c-e24c-43b7-9f4a-75dbb43b349e" />
### Tablolar ve Alan Açıklamaları
 
#### `hasta`
Sistemin temel varlığı. Tüm klinik, genetik ve risk verileri bu tabloya bağlıdır.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `hasta_id` | UUID (PK) | Birincil anahtar |
| `tc_kimlik_no` | VARCHAR (UK) | TC kimlik no, benzersiz |
| `ad`, `soyad` | VARCHAR | İsim bilgileri |
| `dogum_tarihi` | DATE | Doğum tarihi |
| `cinsiyet` | VARCHAR | Cinsiyet |
| `kan_grubu` | VARCHAR | Kan grubu |
| `telefon`, `email` | VARCHAR | İletişim bilgileri |
| `olusturma_tarihi` | TIMESTAMP | Kayıt oluşturma zamanı |
 
---
 
#### `doktor`
Sisteme kayıtlı sağlık profesyonelleri.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `doktor_id` | UUID (PK) | Birincil anahtar |
| `ad`, `soyad` | VARCHAR | İsim bilgileri |
| `uzmanlik_alani` | VARCHAR | Uzmanlık dalı |
| `lisans_no` | VARCHAR (UK) | Lisans numarası, benzersiz |
| `hastane_id` | UUID (FK) | Bağlı olduğu hastane |
| `email` | VARCHAR | İletişim |
 
---
 
#### `hastane`
Doktorların bağlı olduğu kurumlar.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `hastane_id` | UUID (PK) | Birincil anahtar |
| `ad` | VARCHAR | Hastane adı |
| `adres`, `sehir` | VARCHAR | Konum bilgileri |
| `akreditasyon_no` | VARCHAR | Akreditasyon numarası |
 
---
 
#### `tibbi_kayit`
Tüm klinik veri akışının merkezi. Her muayene/ziyaret bir kayıt üretir.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `kayit_id` | UUID (PK) | Birincil anahtar |
| `hasta_id` | UUID (FK) | İlgili hasta |
| `doktor_id` | UUID (FK) | Kaydı oluşturan doktor |
| `ziyaret_tarihi` | TIMESTAMP | Ziyaret zamanı |
| `sikayet` | TEXT | Hastanın şikayeti |
| `tani_notu` | TEXT | Serbest metin tanı notu |
| `tedavi_notu` | TEXT | Tedavi planı |
| `kayit_turu` | VARCHAR | Poliklinik / Yatış / Acil |
 
---
 
#### `tani`
ICD-10 kodlu standart tanı kayıtları. Bir tıbbi kayda birden fazla tanı eklenebilir.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `tani_id` | UUID (PK) | Birincil anahtar |
| `kayit_id` | UUID (FK) | Bağlı tıbbi kayıt |
| `icd10_kodu` | VARCHAR | Uluslararası hastalık kodu |
| `tani_adi` | VARCHAR | Tanı adı |
| `siddet` | VARCHAR | Hafif / Orta / Ağır |
| `tani_tarihi` | DATE | Tanı tarihi |
| `aktif` | BOOLEAN | Aktif hastalık mı? |
 
---
 
#### `ilac_recete` ve `ilac_kalemi`
Reçete yönetimi iki katmanlıdır: üst düzey reçete başlığı (`ilac_recete`) ve her ilaç için ayrı satır (`ilac_kalemi`). İlaçlar ATC kodları ile standartlaştırılır.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `atc_kodu` | VARCHAR | Uluslararası ilaç sınıflandırması |
| `dozaj` | VARCHAR | Doz bilgisi |
| `kullanim_sikli` | VARCHAR | Günde 2x vb. |
| `sure_gun` | INT | Tedavi süresi (gün) |
 
---
 
#### `tibbi_goruntu`
DICOM standardına uygun görüntüleme verisi. Ham görüntü dosyaları HDFS'de şifreli saklanır; tabloda yalnızca metadata ve referans yolu tutulur.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `goruntu_turu` | VARCHAR | MRI / CT / X-Ray / USG |
| `dicom_uid` | VARCHAR (UK) | Evrensel DICOM kimliği |
| `depolama_yolu` | VARCHAR | HDFS dosya yolu |
| `sifreleme_anahtari` | VARCHAR | AES anahtar referansı |
| `radyolog_raporu` | TEXT | Radyolog değerlendirmesi |
 
---
 
#### `lab_test` ve `lab_sonuc`
Laboratuvar verileri iki katmanlıdır: test başlığı ve her parametre için ayrı sonuç satırı. LOINC kodları standart kodlamayı sağlar.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `loinc_kodu` | VARCHAR | Standart laboratuvar kodu |
| `referans_min/max` | FLOAT | Normal değer aralığı |
| `yorum` | VARCHAR | Normal / Düşük / Yüksek / Kritik |
 
---
 
#### `genetik_profil` ve `genetik_varyant`
Ham genomik dosya dış depolamada şifreli saklanır. Klinik önemi olan varyantlar `genetik_varyant` tablosuna işlenir.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `analiz_turu` | VARCHAR | WGS / WES / SNP Panel |
| `rsid` | VARCHAR | dbSNP referans ID |
| `klinik_onemi` | VARCHAR | Patojenik / Benign / Belirsiz |
| `risk_skoru` | FLOAT | Varyant bazlı risk değeri |
 
---
 
#### `risk_degerlendirme`
ML modelleri tarafından hesaplanan hastalık risk skorları. Model versiyonu ve hesaplama zamanı kaydedilerek sonuçların izlenebilirliği sağlanır.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `hastalik_adi` | VARCHAR | Değerlendirilen hastalık |
| `risk_skoru` | FLOAT | 0.0 – 1.0 arası skor |
| `risk_kategorisi` | VARCHAR | Düşük / Orta / Yüksek |
| `model_versiyonu` | VARCHAR | Hangi model sürümü kullanıldı |
 
---
 
#### `oneri`
Risk değerlendirmelerinden türetilen kişiselleştirilmiş tedavi ve yaşam tarzı önerileri.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `oneri_turu` | VARCHAR | Tarama / Yaşam tarzı / İlaç / Sevk |
| `icerik` | TEXT | Öneri metni |
| `oncelik` | INT | 1 (en yüksek) – 5 (en düşük) |
| `gosterildi` | BOOLEAN | Hastaya gösterildi mi? |
 
---
 
#### `hasta_onayi`
KVKK ve GDPR uyumu için her veri işleme türü için ayrı, versiyonlu onay kaydı tutulur.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `onay_turu` | VARCHAR | Tedavi / Araştırma / Genetik / Pazarlama |
| `onay_verildi` | BOOLEAN | Onay durumu |
| `versiyon` | INT | Onay formu versiyonu |
| `ip_adresi` | VARCHAR | Dijital iz |
 
---
 
#### `denetim_kaydi`
Tüm tablolardaki her değişiklik bu tabloya yazılır. Kimin, ne zaman, neyi değiştirdiği eksiksiz izlenir.
 
| Alan | Tip | Açıklama |
|---|---|---|
| `tablo_adi` | VARCHAR | Değişiklik yapılan tablo |
| `islem_turu` | VARCHAR | INSERT / UPDATE / DELETE |
| `onceki_deger` | TEXT | Önceki veri (JSON) |
| `yeni_deger` | TEXT | Yeni veri (JSON) |
 
---
 
### Tasarım Kararları
 
**Neden UUID?**
Dağıtık sistemlerde (Spark, mikroservisler) çakışmasız ID üretimi için UUID kullanıldı; integer auto-increment yerine tercih edildi.
 
**Neden görüntü ve genetik dosyalar tabloda değil?**
DICOM ve genomik dosyalar GB boyutlarına ulaşabileceğinden ham veriler HDFS'de şifreli olarak saklanır. Tablolarda yalnızca metadata ve dosya yolu tutulur.
 
**Neden lab testi iki tabloya ayrıldı?**
Tam kan sayımı gibi bir test 20+ parametre içerebilir. `lab_test` başlık, `lab_sonuc` her parametre için ayrı satır tutar; bu yapı sorgulama ve normalizasyon açısından daha verimlidir.
 
**Neden `denetim_kaydi` ayrı tablo?**
Trigger tabanlı audit log tüm tablolarda tek noktadan değişiklik izlenmesini sağlar; KVKK denetimlerinde veri erişim geçmişi ispatlanabilir hale gelir.
 
---
 
## 🔒 Güvenlik Notları
 
- Tüm kişisel veriler sütun düzeyinde şifreleme ile korunur
- Genetik ve görüntüleme verileri AES-256 ile şifreli depolanır
- Her veri erişimi `denetim_kaydi` tablosuna yazılır
- `hasta_onayi` tablosu KVKK Madde 5-6 ve GDPR Article 9 gerekliliklerini karşılar
- Üretim ortamında `tc_kimlik_no` ve `email` gibi alanlar tokenize edilmelidir
 
---

## 4.Hafta

---
 
## 🔍 Hafta 3 Gözden Geçirme — Tespit Edilen Sorunlar
 
Hafta 2/3'te oluşturulan `data_cleaning_pipeline.py` incelenerek aşağıdaki eksikler ve hatalar saptanmıştır:
 
### 🔴 Kritik Hatalar
 
| # | Sorun | Etki | Dosya / Satır |
|---|-------|------|---------------|
| 1 | `fillna(inplace=True)` Pandas 3.x'te copy üzerinde çalışmıyor | Eksik değerler hiç doldurulmuyordu | `handle_missing_values` |
| 2 | `LabelEncoder` mapping'i kaydedilmiyordu | Her çalıştırmada kategorilere farklı kod atanıyordu (tekrarlanamaz sonuçlar) | `encode_categoricals` |
| 3 | `MinMaxScaler` fit+transform ayrılmamıştı | Test verisinde `fit()` çağrılıyordu → veri sızıntısı (data leakage) riski | `normalize_numeric` |
 
### 🟡 Eksik Özellikler
 
| # | Eksik | Etki |
|---|-------|------|
| 4 | Veri tipi tutarsızlıklarına otomatik müdahale yoktu | `"123.4"` gibi string sayılar LabelEncoder'ı bozuyordu |
| 5 | Metin standardizasyonu yoktu | `"Erkek"`, `"ERKEK"`, `" erkek "` → 3 ayrı kategori sayılıyordu |
| 6 | Sadece IQR aykırı değer yöntemi vardı | Dağılımı farklı sütunlarda yetersiz kalıyordu |
| 7 | Aykırı değerler yalnızca kaldırılabiliyordu | Klinik veride satır kaybetmek yerine sınırlamak daha uygun |
| 8 | Çarpıklık (skewness) tespiti ve düzeltme yoktu | Yüksek skew'lı lab değerleri ML modelini olumsuz etkileyecekti |
| 9 | KVKK hash'inde salt kullanılmıyordu | Rainbow table saldırısına karşı savunmasızdı |
| 10 | Doğrulama kuralları sadece aralık ve izin listesi içeriyordu | Regex, boş olamaz ve çapraz alan kuralları eksikti |
 
---
 
## ✅ Yapılan İyileştirmeler (`data_cleaning_pipeline_v2.py`)
 
### 1. Pandas 3.x Uyumluluğu — `fillna` Düzeltmesi
 
```python
# ❌ Eski (Hafta 2/3) — Pandas 3.x'te çalışmıyor
df[col].fillna(fill_val, inplace=True)
 
# ✅ Yeni — atama ile düzeltildi
df[col] = df[col].fillna(fill_val)
```
 
### 2. Veri Tipi Düzeltme — `fix_data_types` [YENİ]
 
Sayı gibi görünen `object` sütunları otomatik olarak sayısala dönüştürülür. Manuel `type_map` ile tarih ve boolean dönüşümleri de desteklenir:
 
```python
fix_data_types(df, type_map={"giris_tarihi": "datetime", "aktif": "bool"})
```
 
### 3. Metin Standardizasyonu — `clean_text_columns` [YENİ]
 
Büyük/küçük harf, baştaki/sondaki boşluk ve özel karakter tutarsızlıklarını giderir:
 
```python
# Öncesi: "Erkek", "ERKEK", " erkek " → 3 benzersiz kategori
# Sonrası: "Erkek", "Erkek", "Erkek"  → 1 kategori
clean_text_columns(df, ["cinsiyet", "kan_grubu"])
```
 
### 4. Tarih Standardizasyonu — `standardize_dates` [YENİ]
 
Farklı formatlardaki (`DD/MM/YYYY`, `DD.MM.YYYY`, `YYYY-MM-DD`) tarih sütunlarını tek formata çevirir:
 
```python
standardize_dates(df, ["giris_tarihi"], fmt="%Y-%m-%d")
```
 
### 5. Skewness'a Göre Akıllı Eksik Değer Doldurma [İYİLEŞTİRİLDİ]
 
Hafta 2'de her sayısal sütuna medyan uygulanıyordu. Yeni versiyonda dağılım skewness'a göre değerlendirilir:
 
```python
# |skew| > 1 → medyan (aykırı değerlerden etkilenmez)
# |skew| ≤ 1 → ortalama
fill_val = df[col].median() if abs(df[col].skew()) > 1 else df[col].mean()
```
 
### 6. Çift Yöntemli Aykırı Değer Tespiti [İYİLEŞTİRİLDİ]
 
Z-Score yöntemi eklendi; `method="both"` ile her iki yöntem birleştirilebilir. `action="cap"` ile kaldırma yerine sınır değere çekme de desteklenir:
 
```python
# IQR + Z-Score birleşimi, kaldırma yerine sınırlandırma (klinik veriye uygun)
handle_outliers(df, ["sistolik_kb"], method="both", action="cap")
```
 
### 7. Log1p Çarpıklık Düzeltme — `fix_skewness` [YENİ]
 
Enzim değerleri, laboratuvar sonuçları gibi sağa çarpık dağılımlı sütunlara log1p dönüşümü uygulanır:
 
```python
# Öncesi: skewness = 15.57 (aşırı sağa çarpık)
# Sonrası: skewness = -0.14 (normale yakın)
df, transformed = fix_skewness(df, ["enzim_degeri"], threshold=1.0)
```
 
### 8. LabelEncoder Mapping Kaydı [DÜZELTİLDİ]
 
Artık her encoding işleminden sonra `mapping_dict` döndürülür ve JSON raporuna yazılır:
 
```python
df, encoders, mappings = encode_categoricals(df, ["cinsiyet"])
# mappings["cinsiyet"] = {"Erkek": 0, "Kadın": 1, "Bilinmiyor": 2}
```
 
### 9. Scaler Train/Test Ayrımı [DÜZELTİLDİ]
 
Scaler fit edilmiş halde döndürülür; test setine sadece `transform` uygulanır:
 
```python
# Train seti
train_df, scaler = normalize_numeric(train_df, columns, method="minmax")
 
# Test seti — aynı scaler, yeniden fit YOK
test_df, _ = normalize_numeric(test_df, columns, scaler=scaler)
```
 
### 10. Salt ile Anonimleştirme [İYİLEŞTİRİLDİ]
 
```python
# ❌ Eski: SHA256(tc_kimlik_no) → rainbow table ile kırılabilir
# ✅ Yeni: SHA256(salt + tc_kimlik_no) → salt olmadan eşleştirilemez
anonymize_columns(df, ["tc_kimlik_no"], salt="bayt_bukuculer_2025")
```
 
### 11. Genişletilmiş Doğrulama Kuralları [GENİŞLETİLDİ]
 
```python
validation_rules = {
    "yas":          {"min": 0, "max": 120, "not_null": True},      # Boş olamaz
    "email":        {"regex": r"^[\w\.\-]+@[\w\-]+\.[a-z]{2,}$"}, # Format kontrolü
    "diastolik_kb": {                                               # Çapraz alan kuralı
        "cross_field": {"field": "diastolik_kb", "op": "<", "target": "sistolik_kb"}
    },
}
```
 
---
 
## 🧪 Test Sonuçları
 
Test verisi: **500 sentetik hasta kaydı** (bilinçli olarak hatalar, aykırı değerler ve eksikler içeriyor)
 
```
=================================================================
  BAYT BÜKÜCÜLER — HAFTA 4 TEST SÜİTİ
=================================================================
 
📦 Test verisi üretiliyor (n=500)...
   ✓ 500 satır, 15 sütun
 
─────────────────────────────────────────────────────────────────
  TEST ADI                                   SONUÇ
─────────────────────────────────────────────────────────────────
  Veri Tipi Düzeltme                         ✅
  Metin Temizleme                            ✅  6 → 3 benzersiz kategori
  Tarih Standardizasyonu                     ✅  YYYY-MM-DD formatına dönüştürüldü
  Eksik Değer Doldurma                       ✅  246 eksik → 0
  Aykırı Değer — IQR Kaldırma               ✅  500 → 497 satır
  Aykırı Değer — IQR Cap                    ✅  Satır kaybı yok, max_yas = 110.1
  Aykırı Değer — Z-Score                    ✅  enzim_degeri: 8000 → 451 max
  Çarpıklık Düzeltme                         ✅  skewness: 15.57 → -0.14
  Kategorik Mapping Kaydı                    ✅  {"Erkek": 0, "Kadın": 1, ...}
  Scaler Ayrımı (No Leakage)                ✅  Fit sadece train'de
  Çapraz Alan Doğrulaması                    ✅  diastolik < sistolik kuralı
  Anonimleştirme (Salt)                      ✅  Farklı salt → farklı hash
  Tam Pipeline v2                            ✅  500 → 480 satır, 0 eksik
─────────────────────────────────────────────────────────────────
  TOPLAM: 13/13 geçti  🎉 Tüm testler geçti!
=================================================================
```
 
### Pipeline Özet Metrikleri (500 satır test verisi)
 
| Metrik | Değer |
|--------|-------|
| Başlangıç satır sayısı | 500 |
| Temizleme sonrası satır sayısı | 480 |
| Kaldırılan satır oranı | %4.0 |
| Temizleme öncesi eksik sütun sayısı | 7 |
| Temizleme sonrası eksik sütun sayısı | 0 |
| Enzim değeri skewness (öncesi) | 15.57 |
| Enzim değeri skewness (sonrası) | -0.14 |
| Cinsiyet benzersiz değer (öncesi) | 6 |
| Cinsiyet benzersiz değer (sonrası) | 3 |
 
---
 
## 📁 Dosya Yapısı
 
```
bayt-bukuculer/
├── hafta4/
│   ├── data_cleaning_pipeline_v2.py   # Geliştirilmiş pipeline  ← bu hafta
│   ├── test_pipeline.py               # Test süiti              ← bu hafta
│   └── data/
│       ├── test_hasta_kayitlari.csv   # Otomatik üretilen test verisi
│       ├── test_temizlenmis_v2.csv    # Pipeline çıktısı
│       ├── test_cleaning_report_v2.json  # Detaylı temizleme raporu
│       ├── test_raporu.json           # Test sonuçları
│       └── pipeline_v2.log           # Çalışma logu
├── hafta2/
│   └── data_cleaning_pipeline.py     # Önceki versiyon (referans)
└── README.md
```
 
---
 
## 🚀 Kullanım
 
```bash
# Bağımlılıkları yükle
pip install pandas numpy scikit-learn scipy
 
# Testleri çalıştır
python hafta4/test_pipeline.py
 
# Pipeline'ı kendi verinizle kullanın
python -c "
from hafta4.data_cleaning_pipeline_v2 import run_pipeline_v2
result = run_pipeline_v2(
    input_path='data/hasta_kayitlari.csv',
    output_path='data/temiz.csv',
    text_columns=['cinsiyet', 'kan_grubu'],
    outlier_columns=['yas', 'sistolik_kb'],
    outlier_method='both',
    outlier_action='cap',
    sensitive_columns=['tc_kimlik_no', 'email'],
)
"
```
 
---

*Bu README proje ilerledikçe güncellenecektir.*
