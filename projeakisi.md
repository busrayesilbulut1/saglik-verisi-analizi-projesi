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
## 4. Hafta
# 🔍 Hafta 4: Veri Güvenliği ve Gizliliği Kontrolleri

Bu çalışma, sistemde uygulanan hassas veri koruma tekniklerinin (maskeleme, anonimleştirme, erişim kontrolü) etkinliğini değerlendirmek, yasal uyumluluğu denetlemek ve sistem güvenliğini optimize etmek amacıyla hazırlanmıştır.

---

## 1. Uygulanan Tekniklerin Etkinlik Değerlendirmesi

| Teknik | Mevcut Durum | Etkinlik Analizi | Risk Seviyesi |
| :--- | :--- | :--- | :---: |
| **Veri Maskeleme** | Statik maskeleme (örn: TC No: 123*****890) | UI seviyesinde etkili fakat veritabanı sorgularında sızıntı riski taşıyor. | Düşük |
| **Anonimleştirme** | K-Anonimlik ($k=5$) | Veri seti küçüldükçe "Outlier" (aykırı) hastaların tespit edilme riski artıyor. | Orta |
| **Erişim Kontrolü** | Rol Tabanlı (RBAC) | Yetki tanımları net ancak "Privilege Escalation" (yetki yükseltme) testleri eksik. | Orta |
| **Şifreleme** | AES-256 (At Rest) | Anahtar yönetimi (Key Management) merkezi bir noktada toplandığı için tekil hata noktası riski var. | Düşük |

---

## 2. Mevcut Politikalara Uyumluluk Denetimi (Audit)

Projenin **GDPR (KVKK)** ve **HIPAA** standartlarına uyumluluğu aşağıdaki kriterlere göre denetlenmiştir:

- [x] **Veri Minimizasyonu:** Sadece analiz için gerekli olan "yaş, semptom, şehir" verileri işleniyor; "isim, adres" gibi doğrudan tanımlayıcılar işlem dışı bırakılıyor.
- [ ] **Unutulma Hakkı:** Veritabanından bir hastanın verisinin kalıcı ve iz bırakmadan silinmesi için gerekli olan "Shredding" (veri imhası) prosedürü henüz otomatize edilmedi.
- [x] **Veri Taşınabilirliği:** Veriler, standart JSON/CSV formatında şifreli olarak dışa aktarılabiliyor.

---

## 3. İyileştirme ve Optimizasyon Önerileri

Sistemin savunma hattını güçlendirmek için aşağıdaki geliştirmelerin yapılması planlanmaktadır:

### 🛡️ Sıfır Güven (Zero Trust) Yaklaşımı
Sadece ağın içinde olmayı güvenli kabul etmek yerine, sistem içindeki her mikroservis arası veri alışverişinde mTLS (Mutual TLS) kullanarak her adımda kimlik doğrulama yapılmalıdır.

### 🧪 Diferansiyel Gizlilik (Differential Privacy) Entegrasyonu
Anonimleştirme sırasında veriye istatistiksel gürültü ekleyerek, veri setinden tek bir kişinin varlığının veya yokluğunun sorgu sonuçlarını etkilememesi sağlanacaktır. Bu, "Linkage Attack" (veri eşleştirme saldırıları) riskini sıfıra indirir.

### 📜 Dinamik Maskeleme
Kullanıcının yetkisine göre verinin çalışma anında (runtime) maskelenmesi sağlanmalıdır. Örneğin; bir hemşire hastanın yaşını görebilirken, bir idari personelin bu alanı sadece aralık (örn: 20-30 yaş arası) olarak görmesi sağlanacaktır.

---

## 4. Teknik Aksiyon Planı (Action Items)

1. **Denetim:** `Audit Log` modülünün, sistem yöneticisinin bile silemeyeceği "Write-Once-Read-Many" (WORM) depolama birimine yönlendirilmesi.
2. **Test:** Anonimleştirilmiş veri setleri üzerinde "Attack Simulation" (Saldırı Simülasyonu) yapılarak verinin ne kadar sürede de-anonimize edilebileceğinin ölçülmesi.
3. **Uyum:** KVKK uyarınca hazırlanan "Veri İşleme Envanteri"nin kod seviyesinde dökümante edilmesi.

---
## 5. Hafta
# 📈 Hafta 5: Model Performansını Değerlendirme ve İyileştirme

Bu döküman, geliştirilen tahminleme modelinin performans metriklerini, sistemin güvenliğini (Adversarial ML) ve veri bütünlüğünü koruyacak şekilde değerlendirmek ve optimize etmek amacıyla hazırlanmıştır. 

## 1. Güvenli Performans Değerlendirme Metrikleri

Modelin başarısı, sadece temiz verilerle değil, aynı zamanda olası veri manipülasyonlarına karşı direncini de ölçecek şekilde analiz edilmiştir.

### 🛡️ Güvenli Stabilite Analizi
*   **Adversarial Robustness (Saldırgan Dayanıklılığı):** Modelin, giriş verilerine eklenen küçük "gürültülere" (noise) karşı verdiği tepki ölçülmüştür. Amaç, kötü niyetli verilerle modelin yanlış teşhis koymasının önüne geçmektir.
*   **Cross-Validation & Variance Check:** Veri seti 5 parçaya bölünerek (K-Fold) test edilmiş ve varyansın ($\sigma^2$) düşük tutulması sağlanmıştır. Yüksek varyans, modelin belirli veri alt kümelerine aşırı duyarlı (overfitting) olduğunu ve manipülasyona açık olduğunu gösterir.

| Metrik | Mevcut Durum | Güvenli Hedef | Önem Derecesi |
| :--- | :---: | :---: | :--- |
| **Recall (Duyarlılık)** | %76 | %92+ | 🚨 Kritik (Hayati) |
| **F1-Score Kararlılığı** | $\pm \%5$ | $\pm \%1$ | 🛠️ Sistem Güvenilirliği |
| **Adversarial Error Rate** | %18 | <%5 | 🛡️ Güvenlik |
| **Inference Latency** | 450ms | <150ms | ⚡ DoS Direnci |

---

## 2. Güvenli Model İyileştirme ve Parametre Ayarları

Modelin doğruluk oranını artırmak için yapılan müdahaleler, "Model Poisoning" (Model Zehirlenmesi) riskini minimize edecek şekilde tasarlanmıştır.

### 🛠️ Hiperparametre Optimizasyonu (Secure Tuning)
*   **Bayesian Optimization:** Grid Search yerine daha verimli olan Bayesyen arama kullanılarak, modelin hiperparametreleri (örn: `learning_rate`, `n_estimators`) en kararlı ve güvenli noktaya çekilmiştir.
*   **Gradient Clipping:** Derin öğrenme veya gradyan tabanlı modellerde, gradyan patlamalarını ve bu yolla yapılabilecek manipülasyonları engellemek için gradyan sınırlama tekniği uygulanmıştır.

### 🔄 Algoritma Değişiklikleri
*   **Ensemble Robustness:** Tekil karar ağaçları yerine **XGBoost** veya **Random Forest** gibi topluluk yöntemleri tercih edilerek, tek bir veri noktasına duyarlılık azaltılmış ve sistemin genel direnci artırılmıştır.
*   **Differential Privacy in Training:** Model eğitimi sırasında veriye kontrollü gürültü eklenerek, modelin belirli kişisel verileri "ezberlemesi" (memorization) engellenmiş ve veri gizliliği korunmuştur.

---

## 3. Model Bütünlüğü ve Güvenli Güncelleme (Integrity)

Modelin parametreleri güncellenirken ve test edilirken şu güvenlik protokolleri takip edilir:

*   **Secure Model Serialization:** Model dosyaları (`.pkl`, `.h5`) kaydedilirken ve yüklenirken, "Insecure Deserialization" açıklarını önlemek için güvenli kütüphaneler kullanılacak ve model dosyaları **SHA-256** ile imzalanacaktır.
*   **Model Versioning (Governance):** Yapılan her parametre değişikliği ve model güncellemesi bir versiyon takip sisteminde (DVC gibi) tutularak, yetkisiz bir değişikliğin veya "model drift" olayının anında tespiti sağlanacaktır.
*   **Outlier Detection:** Değerlendirme sırasında, modelin tahminlerini aşırı derecede saptıran "outlier" veriler otomatik olarak işaretlenerek siber güvenlik analizi için loglanacaktır.

---

## 4. Uygulanan Teknik Aksiyonlar

### A. Robust Scaling
Aykırı değerlerin sistemi manipüle etmemesi için `StandardScaler` yerine medyan bazlı **`RobustScaler`** kullanımı standartlaştırılmıştır:
$$z = \frac{x_i - Q_2(x)}{Q_3(x) - Q_1(x)}$$

### B. Otomatik Eşik (Threshold) Yönetimi
Modelin "hasta/sağlıklı" ayrımını yaptığı olasılık eşiği, sadece doğruluğu değil, **False Negative** maliyetini ve güvenlik risklerini de hesaplayan bir maliyet fonksiyonu ile optimize edilmiştir.

---

