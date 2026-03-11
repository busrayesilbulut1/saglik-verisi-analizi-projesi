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
