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

## 3. Hafta
# 🛡️ Hafta 3: Veri Güvenliği ve Gizlilik Protokolleri Tasarımı

Bu döküman, **Sağlık Verisi Analizi ve Tahminleme Sistemi** kapsamında işlenen hassas hasta verilerinin güvenliğini sağlamak, yasal uyumluluk (GDPR, HIPAA, KVKK) kriterlerini karşılamak ve olası veri ihlallerini önlemek amacıyla tasarlanmıştır.

## 1. Yasal ve Etik Uyum Çerçevesi
Sistem, "Privacy by Design" (Tasarım Yoluyla Gizlilik) prensibiyle aşağıdaki standartlara tam uyumlu geliştirilecektir:
*   **GDPR/KVKK:** Veri minimizasyonu, unutulma hakkı ve veri işleme envanteri yönetimi.
*   **HIPAA:** Sağlık verilerinin (PHI - Protected Health Information) korunması, teknik ve idari güvenlik önlemleri.

---

## 2. Temel Güvenlik Protokolleri

### 🔐 Veri Şifreleme (Data Encryption)
Veriler, yaşam döngüsünün her aşamasında şifrelenmiş halde tutulacaktır:
*   **Data at Rest (Depolama):** Veritabanı ve HDFS (Hadoop Distributed File System) katmanında veriler **AES-256** simetrik şifreleme algoritması ile saklanacaktır. Anahtar yönetimi için KMS (Key Management Service) kullanılacaktır.
*   **Data in Transit (Aktarım):** Sunucu ile istemci arasındaki ve mikroservislerin kendi arasındaki tüm trafik **TLS 1.3** protokolü ve SSL sertifikaları ile şifrelenecektir.

### 🔑 Erişim Kontrolü ve Kimlik Doğrulama
*   **RBAC (Role-Based Access Control):** "En Az Ayrıcalık" (Least Privilege) ilkesi uygulanacaktır.
    *   *Doktorlar:* Sadece sorumlu oldukları hastaların tıbbi kayıtlarına erişebilir.
    *   *Veri Analistleri:* Sadece anonimleştirilmiş veri setlerine (PII içermeyen) erişebilir.
*   **MFA (Multi-Factor Authentication):** Sisteme girişlerde statik şifrelerin yanı sıra TOTP veya SMS tabanlı ikinci bir doğrulama katmanı zorunlu olacaktır.
*   **Zaman Sınırlı Erişim:** Kritik verilere erişim yetkileri belirli sürelerle sınırlandırılacak ve otomatik oturum sonlandırma (Session Timeout) uygulanacaktır.

### 📝 Denetim İzleri ve İzleme (Audit Trails)
*   Sistemdeki her türlü veri erişimi, değişikliği ve silme işlemi; kullanıcı kimliği, işlem türü, kaynak IP ve zaman damgası (Timestamp) ile birlikte loglanacaktır.
*   Log kayıtları değiştirilemez (Immutable) bir yapıda tutulacak ve periyodik olarak siber güvenlik denetimlerinden geçirilecektir.

---

## 3. Veri Gizliliği ve Anonimleştirme Teknikleri

Analiz ve tahminleme süreçlerinde hasta gizliliğini korumak için aşağıdaki yöntemler uygulanacaktır:

| Teknik | Açıklama | Uygulama Amacı |
| :--- | :--- | :--- |
| **Psödonimleştirme** | İsim, TC No gibi doğrudan tanımlayıcıların geri döndürülebilir bir "token" ile maskelenmesi. | Operasyonel Veri İşleme |
| **K-Anonimlik** | Veri setindeki her bir kaydın en az $k-1$ adet başka kayıtla ayırt edilemez hale getirilmesi. | İstatistiksel Analiz |
| **Diferansiyel Gizlilik** | Veriye kontrollü gürültü (noise) ekleyerek tekil bireylerin tespit edilmesini imkansız kılma. | Model Eğitimi |
| **Veri Maskeleme** | Kredi kartı veya kimlik numaralarının sadece son 4 hanesinin gösterilmesi. | Arayüz Görüntüleme |

---

## 4. Risk Değerlendirmesi ve Güvenlik Açığı Analizi

Sistemin savunmasız kalabileceği noktalar ve alınan önlemler:

| Risk Tanımı | Etki | Olasılık | Önleyici Faaliyet |
| :--- | :---: | :---: | :--- |
| **SQL Injection / XSS** | Kritik | Düşük | Input validation, parameterized queries ve WAF kullanımı. |
| **Kayıp/Çalıntı Cihazlar** | Yüksek | Orta | Uç nokta şifrelemesi ve uzaktan veri silme protokolleri. |
| **Yetersiz Log Denetimi** | Orta | Orta | SIEM (Security Information and Event Management) entegrasyonu. |
| **Brute Force Atakları** | Orta | Yüksek | IP tabanlı Rate Limiting ve Account Lockout politikaları. |

---

## 5. Uygulama Planı (Checklist)
- [ ] PyCryptodome kullanılarak veritabanı seviyesinde şifreleme modüllerinin geliştirilmesi.
- [ ] OAuth 2.0 + JWT tabanlı güvenli oturum yönetiminin kurulması.
- [ ] Spark üzerinde veri işleme sırasında kişisel verileri filtreleyen anonimleştirme fonksiyonlarının yazılması.
- [ ] Olası bir veri ihlali durumunda uygulanacak olan "Olay Müdahale Planı"nın (Incident Response Plan) oluşturulması.

---

