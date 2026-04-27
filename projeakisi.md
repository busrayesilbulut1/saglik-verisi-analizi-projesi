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
* **Hız Hedefi:** Kullanıcı deneyimi açısından hasta dashboard'u ve raporlama ekranlarının ≤5 saniyede yüklenmesini hedefliyoruz. DICOM görüntü analizi ve model inference gibi işlemler asenkron çalışacağından bu hedefin kapsamı dışındadır.

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

Bu haftaki görev kapsamında, projedeki sağlık verilerini (klinik kayıtlar, laboratuvar sonuçları, risk skorları) anlamlı biçimde sunabilmek için farklı görselleştirme araçlarını inceledim. Değerlendirmemi 1. haftada belirlenen paydaş beklentileri ve performans hedefleri üzerine kurdum: doktorların hızla yorumlayabileceği, ≤5 saniyede yüklenen, KVKK uyumlu bir arayüz.

#### 1. İncelenen Araçlar

#### Tableau

Tableau, sürükle-bırak arayüzüyle etkileşimli dashboard oluşturmaya odaklanan bir iş zekası platformudur.

| | |
| :--- | :--- |
| **Avantajları** | Kod yazmadan karmaşık filtreler ve drill-down görünümleri oluşturulabilir; büyük veri kaynaklarıyla (Spark, SQL) canlı bağlantı kurulabilir; şablon kütüphanesi geniştir. |
| **Dezavantajları** | Lisans maliyeti yüksektir; özel Python/ML entegrasyonu dolaylı yollarla (TabPy) yapılmaktadır; DICOM veya genomik dosyaları doğrudan işleyemez. |

#### Microsoft Power BI

Power BI, Microsoft ekosistemiyle sıkı entegrasyona sahip, düşük maliyetli bir görselleştirme aracıdır.

| | |
| :--- | :--- |
| **Avantajları** | Azure veri servisleriyle doğrudan bağlantı kurulabilir; DAX formülleriyle hesaplanmış metrikler tanımlanabilir; Power Query ile basit ETL adımları uygulanabilir. |
| **Dezavantajları** | Karmaşık istatistiksel görselleştirmeler için eklenti gerektirir; Türkiye KVKK kapsamında bulut veri konumu dikkatle yönetilmelidir. |

#### Plotly / Dash

Plotly, Python tabanlı etkileşimli grafikler; Dash ise bu grafikleri web uygulamasına dönüştüren bir framework sunar.

| | |
| :--- | :--- |
| **Avantajları** | Tamamen ücretsiz ve açık kaynaklıdır; scikit-learn, TensorFlow ve Pandas ile doğrudan entegre çalışır; özelleştirme esnekliği yüksektir. |
| **Dezavantajları** | Tasarımcı dostu değildir; iyi görünümlü bir dashboard için geliştirme süresi uzayabilir; ölçeklenebilirlik için ek yapılandırma gerekir. |

#### Matplotlib / Seaborn

Python'un temel görselleştirme kütüphaneleridir; ağırlıklı olarak veri analizi ve raporlama süreçlerinde kullanılır.

| | |
| :--- | :--- |
| **Avantajları** | Her Python ortamında çalışır; akademik standartlarda yayın kalitesinde grafikler üretilir; öğrenme eğrisi düşüktür. |
| **Dezavantajları** | Statik çıktı üretir, gerçek zamanlı etkileşim yoktur; doktor arayüzü için tek başına yeterli değildir. |

#### Grafana

Zaman serisi verilerini izlemek için tasarlanmış açık kaynaklı bir platform olan Grafana, sağlık sistemlerinde vital bulgu takibinde yaygın kullanılmaktadır.

| | |
| :--- | :--- |
| **Avantajları** | Gerçek zamanlı veri akışı için optimize edilmiştir; alarm ve eşik bildirimi kurulabilir; PostgreSQL, InfluxDB ve Spark ile çalışır. |
| **Dezavantajları** | Klinik rapor veya genetik veri görselleştirmesi için uygun değildir; hasta odaklı dashboard yerine sistem izleme odaklıdır. |

---

#### 2. Araçların Karşılaştırması

| Kriter | Tableau | Power BI | Plotly/Dash | Matplotlib | Grafana |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Python/ML entegrasyonu | Kısmi | Kısmi | Tam | Tam | Kısmi |
| Etkileşimli dashboard | ✅ | ✅ | ✅ | ❌ | ✅ |
| Ücretsiz kullanım | ❌ | Kısmen | ✅ | ✅ | ✅ |
| Gerçek zamanlı veri | ✅ | ✅ | ✅ | ❌ | ✅ |
| Doktor arayüzüne uygunluk | Yüksek | Yüksek | Orta | Düşük | Düşük |
| Spark / büyük veri desteği | ✅ | ✅ | ✅ | ❌ | Kısmi |

---

#### 3. Proje İçin Önerilen Görselleştirme Stratejisi

Tek bir araçta kalmak yerine, her katman için en uygun aracı kullanmak daha verimli bir yaklaşım olacaktır.

#### Doktor Dashboard'u (Gerçek Zamanlı, Etkileşimli)
* **Öneri:** Plotly Dash  
* **Gerekçe:** Projenin Python/scikit-learn/TensorFlow altyapısıyla doğrudan entegre çalışır. Lisans maliyeti yoktur ve API'den gelen tahmin sonuçlarını ≤5 saniyede render edebilir. Doktor arayüzünde kullanılacak risk göstergesi, laboratuvar trendi ve öneri paneli bu araçla geliştirilecektir.

#### Veri Analizi ve Raporlama (Araştırma, Sunum)
* **Öneri:** Matplotlib / Seaborn  
* **Gerekçe:** Model eğitimi ve EDA (Keşifsel Veri Analizi) aşamalarında, istatistiksel dağılım ve korelasyon grafikleri için uygundur. Jupyter Notebook içinde doğrudan çalışır.

#### Yönetim Raporları (Periyodik, Yüksek Seviye)
* **Öneri:** Power BI  
* **Gerekçe:** Azure altyapısıyla entegrasyon kolaylığı ve iş kullanıcılarına yönelik sade arayüzü nedeniyle hastane yönetimine sunulacak periyodik raporlar için tercih edilebilir. KVKK kapsamında veri konumu yönetimi için Azure Türkiye bölgeleri kullanılmalıdır.

---

#### 4. Sağlık Verisine Özgü Görselleştirme Tipleri

Projenin veri yapısına göre aşağıdaki grafik türleri dashboard tasarımında öncelikli olacaktır.

| Görselleştirme | Veri Kaynağı | Kullanım Amacı |
| :--- | :--- | :--- |
| **Risk Göstergesi (Gauge)** | risk_degerlendirme tablosu | Hastanın hastalık riskini 0-100 skalasında tek bakışta gösterir. |
| **Laboratuvar Trendi (Line Chart)** | MIMIC-IV / lab_sonuc tablosu | HbA1c, kreatinin gibi parametrelerin zaman içindeki değişimini izler. |
| **Korelasyon Isı Haritası (Heatmap)** | MIMIC-IV klinik kayıtlar | Laboratuvar parametreleri arasındaki ilişkileri ortaya çıkarır. |
| **Genetik Varyant Dağılımı (Bar/Lollipop)** | TCGA / genetik_varyant tablosu | Klinik öneme göre (Patojenik / Belirsiz / Benign) varyantları sınıflandırır. |
| **Zaman Çizelgesi (Timeline)** | tibbi_kayit + tani + ilac_recete | Hastanın muayene, tanı ve ilaç geçmişini kronolojik olarak sunar. |
| **Risk Faktörü Ağırlığı (Horizontal Bar)** | Tahmin modeli çıktısı | Doktora hangi faktörün riski ne kadar artırdığını açıklar (XAI). |

---

#### 5. Sonuç

Bu hafta yaptığım araştırma, görselleştirme katmanının tek bir araçla değil, katmana göre seçilmiş araç kombinasyonuyla kurulması gerektiğini ortaya koydu. Doktor arayüzü için **Plotly Dash**, analiz süreçleri için **Matplotlib/Seaborn**, yönetim raporlaması için **Power BI** önerilmektedir. Bu strateji, hem maliyet hem de teknik entegrasyon açısından projenin mevcut altyapısıyla en uyumlu yaklaşımdır.

3. haftada tasarlanan UI/UX wireframe'indeki ekranlar, bu araç seçimlerine dayalı olarak şekillendirilmiştir.

---

## 3. Hafta
[ UI/UX Figma Wireframe Tasarımı](https://www.figma.com/design/3Yn5izP8b1waj3hN70nJ0z/Wireframe?node-id=0-1&t=sL417Uu9OZoXaokZ-1)

**Frame 4 Notu:** Zaman Çizelgesi ekranında bir what-if simülasyonu özelliği tasarladım. Bu özellik, farklı tedavi senaryolarının tahmini sonuçlarını karşılaştırmalı olarak sunar. What-if frame'i v2 için tasarlanmıştır. 
