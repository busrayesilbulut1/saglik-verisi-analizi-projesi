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
# 📊 Hafta Görevi: Veri Analizi için Python Kütüphanelerini Derinlemesine İnceleme

Bu haftaki çalışma odağım, projenin veri işleme katmanını daha performanslı ve okunabilir hale getirmek amacıyla **Pandas** ve **NumPy** kütüphanelerinin ileri seviye özelliklerini öğrenmek ve "Health Data Analysis" sistemi için optimize edilmiş bir altyapı tasarlamaktır.

## 🎯 Temel Hedefler
- **Vektörizasyon:** Python döngülerinden (`for`, `while`) kaçınarak işlemleri doğrudan CPU seviyesinde (NumPy kernel) koşturmak ve hızı $100x$ seviyelerine çıkarmak.
- **Hiyerarşik Yapı:** Çok boyutlu sağlık verilerini (Örn: Şehir -> Hastane -> Hasta -> Tarih) yönetmek için **MultiIndex** yapılarını kurgulamak.
- **Pipeline Mimarisi:** Veriyi bir uçtan alıp (raw) diğer uçtan temizlenmiş ve analize hazır (processed) çıkaran zincirleme fonksiyonlar (Method Chaining) tasarlamak.

---

## 🛠️ Teknik Odak Noktaları ve Fonksiyonel Detaylar

### 1. NumPy: Düşük Seviye Performans ve Bellek Yönetimi
- [ ] **Advanced Broadcasting Logic:** Farklı boyutlardaki (Shape) dizilerin birbiriyle eşleşme kurallarını (`stride_tricks`) kullanarak bellek kopyalamadan işlem yapmak.
- [ ] **Masking & Boolean Indexing:** Milyonlarca satırlık veri setinde, belirli kriterlere (Örn: "Kan şekeri > 140 olan tüm hastalar") uyan verileri mikro saniyeler içinde filtrelemek.
- [ ] **Ufuncs & Vectorize:** `np.where()` ve `np.select()` ile karmaşık `if-else` mantıklarını dizi operasyonlarına dönüştürmek.
- [ ] **Memory View:** Veriyi kopyalamak yerine sadece görünümünü (`view` vs `copy`) değiştirerek RAM kullanımını optimize etmek.

### 2. Pandas: Endüstriyel Veri Mühendisliği
- [ ] **Method Chaining & Pipe:** Kod karmaşasını engellemek için `.pipe()`, `.assign()` ve `.query()` metodlarını kullanarak "Fluent Interface" tasarımı uygulamak.
- [ ] **Advanced Aggregation:** `.groupby().agg()` içerisinde sözlük yapıları kullanarak her sütun için farklı istatistiksel (mean, std, unique count) hesaplamalar yapmak.
- [ ] **Multi-Indexing & Reshaping:** 
    *   `stack()` ve `unstack()` ile veriyi dikeyden yataya (ve tersi) dönüştürmek.
    *   `pd.merge_asof()` kullanarak zaman serisi verilerini en yakın zaman dilimine göre birleştirmek.
- [ ] **Categorical Data:** String tabanlı sütunları `category` tipine dönüştürerek bellek kullanımını %80'e kadar azaltmak.

---

## 📚 Kaynaklar ve Notlar
- **Performans Notu:** Büyük veri setlerinde `.apply(lambda x: ...)` kullanımından kaçınılacak, bunun yerine vektörize metodlar tercih edilecektir.
- **Standartlar:** Tüm veri işleme süreçleri için modüler bir yapı korunacak ve "Clean Code" prensiplerine sadık kalınacaktır.
- **Tip Güvenliği:** `numpy.typing` kullanılarak dizi boyutları ve veri tipleri kontrol altında tutulacaktır.

> **Mühendislik Notu:** Bu döküman, projenin ölçeklenebilir (scalable) bir veri analizi altyapısına sahip olması için rehber niteliğindedir.
