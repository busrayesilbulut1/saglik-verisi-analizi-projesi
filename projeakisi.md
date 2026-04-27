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
**Mehmet Boztepe**: Sağlık veri setleri araştırması.

---

## 2. Hafta

Bu haftaki görev kapsamında, projedeki sağlık verilerini (klinik kayıtlar, laboratuvar sonuçları, risk skorları) anlamlı biçimde sunabilmek için farklı görselleştirme araçlarını inceledim. Değerlendirmemi 1. haftada belirlenen paydaş beklentileri ve performans hedefleri üzerine kurdum: doktorların hızla yorumlayabileceği, ≤5 saniyede yüklenen, KVKK uyumlu bir arayüz.

### 1. İncelenen Araçlar

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

### 2. Araçların Karşılaştırması

| Kriter | Tableau | Power BI | Plotly/Dash | Matplotlib | Grafana |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Python/ML entegrasyonu | Kısmi | Kısmi | Tam | Tam | Kısmi |
| Etkileşimli dashboard | ✅ | ✅ | ✅ | ❌ | ✅ |
| Ücretsiz kullanım | ❌ | Kısmen | ✅ | ✅ | ✅ |
| Gerçek zamanlı veri | ✅ | ✅ | ✅ | ❌ | ✅ |
| Doktor arayüzüne uygunluk | Yüksek | Yüksek | Orta | Düşük | Düşük |
| Spark / büyük veri desteği | ✅ | ✅ | ✅ | ❌ | Kısmi |

---

### 3. Proje İçin Önerilen Görselleştirme Stratejisi

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

### 4. Sağlık Verisine Özgü Görselleştirme Tipleri

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

### 5. Sonuç

Bu hafta yaptığım araştırma, görselleştirme katmanının tek bir araçla değil, katmana göre seçilmiş araç kombinasyonuyla kurulması gerektiğini ortaya koydu. Doktor arayüzü için **Plotly Dash**, analiz süreçleri için **Matplotlib/Seaborn**, yönetim raporlaması için **Power BI** önerilmektedir. Bu strateji, hem maliyet hem de teknik entegrasyon açısından projenin mevcut altyapısıyla en uyumlu yaklaşımdır.

3. haftada tasarlanan UI/UX wireframe'indeki ekranlar, bu araç seçimlerine dayalı olarak şekillendirilmiştir.

---

## 3. Hafta
[ UI/UX Figma Wireframe Tasarımı](https://www.figma.com/design/3Yn5izP8b1waj3hN70nJ0z/Wireframe?node-id=0-1&t=sL417Uu9OZoXaokZ-1)

**Frame 4 Notu:** Zaman Çizelgesi ekranında bir what-if simülasyonu özelliği tasarladım. Bu özellik, farklı tedavi senaryolarının tahmini sonuçlarını karşılaştırmalı olarak sunar. What-if frame'i v2 için tasarlanmıştır. 
