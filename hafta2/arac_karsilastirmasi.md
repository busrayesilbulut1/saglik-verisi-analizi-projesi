# Veri Görselleştirme Araçları Karşılaştırması

Bu belge, Sağlık Verisi Analizi ve Tahminleme Sistemi'nin görselleştirme katmanı için
incelenen araçları ve proje için önerilen stratejiyi içerir.
Değerlendirme, Hafta 1'de belirlenen paydaş beklentileri ve performans hedefleri
(≤5 sn yükleme, KVKK uyumu, Python/ML entegrasyonu) üzerine kurulmuştur.

---

## 1. İncelenen Araçlar

### Tableau

Sürükle-bırak arayüzüyle etkileşimli dashboard oluşturmaya odaklanan bir iş zekası platformudur.

| | |
| :--- | :--- |
| **Avantajları** | Kod yazmadan karmaşık filtreler ve drill-down görünümleri oluşturulabilir; büyük veri kaynaklarıyla (Spark, SQL) canlı bağlantı kurulabilir; şablon kütüphanesi geniştir. |
| **Dezavantajları** | Lisans maliyeti yüksektir; özel Python/ML entegrasyonu dolaylı yollarla (TabPy) yapılmaktadır; DICOM veya genomik dosyaları doğrudan işleyemez. |

### Microsoft Power BI

Microsoft ekosistemiyle sıkı entegrasyona sahip, düşük maliyetli bir görselleştirme aracıdır.

| | |
| :--- | :--- |
| **Avantajları** | Azure veri servisleriyle doğrudan bağlantı kurulabilir; DAX formülleriyle hesaplanmış metrikler tanımlanabilir; Power Query ile basit ETL adımları uygulanabilir. |
| **Dezavantajları** | Karmaşık istatistiksel görselleştirmeler için eklenti gerektirir; Türkiye KVKK kapsamında bulut veri konumu dikkatle yönetilmelidir. |

### Plotly / Dash

Plotly, Python tabanlı etkileşimli grafikler; Dash ise bu grafikleri web uygulamasına dönüştüren bir framework sunar.

| | |
| :--- | :--- |
| **Avantajları** | Tamamen ücretsiz ve açık kaynaklıdır; scikit-learn, TensorFlow ve Pandas ile doğrudan entegre çalışır; özelleştirme esnekliği yüksektir. |
| **Dezavantajları** | Tasarımcı dostu değildir; iyi görünümlü bir dashboard için geliştirme süresi uzayabilir; ölçeklenebilirlik için ek yapılandırma gerekir. |

### Matplotlib / Seaborn

Python'un temel görselleştirme kütüphaneleridir; ağırlıklı olarak veri analizi ve raporlama süreçlerinde kullanılır.

| | |
| :--- | :--- |
| **Avantajları** | Her Python ortamında çalışır; akademik standartlarda yayın kalitesinde grafikler üretilir; öğrenme eğrisi düşüktür. |
| **Dezavantajları** | Statik çıktı üretir, gerçek zamanlı etkileşim yoktur; doktor arayüzü için tek başına yeterli değildir. |

### Grafana

Zaman serisi verilerini izlemek için tasarlanmış açık kaynaklı bir platformdur; sağlık sistemlerinde vital bulgu takibinde yaygın kullanılmaktadır.

| | |
| :--- | :--- |
| **Avantajları** | Gerçek zamanlı veri akışı için optimize edilmiştir; alarm ve eşik bildirimi kurulabilir; PostgreSQL, InfluxDB ve Spark ile çalışır. |
| **Dezavantajları** | Klinik rapor veya genetik veri görselleştirmesi için uygun değildir; hasta odaklı dashboard yerine sistem izleme odaklıdır. |

---

## 2. Karşılaştırma Matrisi

| Kriter | Tableau | Power BI | Plotly/Dash | Matplotlib | Grafana |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Python/ML entegrasyonu | Kısmi | Kısmi | Tam | Tam | Kısmi |
| Etkileşimli dashboard | ✅ | ✅ | ✅ | ❌ | ✅ |
| Ücretsiz kullanım | ❌ | Kısmen | ✅ | ✅ | ✅ |
| Gerçek zamanlı veri | ✅ | ✅ | ✅ | ❌ | ✅ |
| Doktor arayüzüne uygunluk | Yüksek | Yüksek | Orta | Düşük | Düşük |
| Spark / büyük veri desteği | ✅ | ✅ | ✅ | ❌ | Kısmi |

---

## 3. Proje İçin Önerilen Görselleştirme Stratejisi

Tek bir araçta kalmak yerine, her katman için en uygun aracı kullanmak daha verimli bir yaklaşımdır.

### Doktor Dashboard'u (Gerçek Zamanlı, Etkileşimli)
- **Öneri:** Plotly Dash
- **Gerekçe:** Projenin Python/scikit-learn/TensorFlow altyapısıyla doğrudan entegre çalışır. Lisans maliyeti yoktur ve API'den gelen tahmin sonuçlarını ≤5 saniyede render edebilir.

### Veri Analizi ve Raporlama (Araştırma, Sunum)
- **Öneri:** Matplotlib / Seaborn
- **Gerekçe:** Model eğitimi ve EDA aşamalarında istatistiksel dağılım ve korelasyon grafikleri için uygundur; Jupyter Notebook içinde doğrudan çalışır.

### Yönetim Raporları (Periyodik, Yüksek Seviye)
- **Öneri:** Power BI
- **Gerekçe:** Azure altyapısıyla entegrasyon kolaylığı ve iş kullanıcılarına yönelik sade arayüzü nedeniyle tercih edilebilir. KVKK kapsamında veri konumu yönetimi için Azure Türkiye bölgeleri kullanılmalıdır.

---

## 4. Sağlık Verisine Özgü Görselleştirme Tipleri

| Görselleştirme | Veri Kaynağı | Kullanım Amacı |
| :--- | :--- | :--- |
| **Risk Göstergesi (Gauge)** | risk_degerlendirme tablosu | Hastanın hastalık riskini 0-100 skalasında tek bakışta gösterir. |
| **Laboratuvar Trendi (Line Chart)** | MIMIC-IV / lab_sonuc tablosu | HbA1c, kreatinin gibi parametrelerin zaman içindeki değişimini izler. |
| **Korelasyon Isı Haritası (Heatmap)** | MIMIC-IV klinik kayıtlar | Laboratuvar parametreleri arasındaki ilişkileri ortaya çıkarır. |
| **Genetik Varyant Dağılımı (Bar/Lollipop)** | TCGA / genetik_varyant tablosu | Klinik öneme göre (Patojenik / Belirsiz / Benign) varyantları sınıflandırır. |
| **Zaman Çizelgesi (Timeline)** | tibbi_kayit + tani + ilac_recete | Hastanın muayene, tanı ve ilaç geçmişini kronolojik olarak sunar. |
| **Risk Faktörü Ağırlığı (Horizontal Bar)** | Tahmin modeli çıktısı | Doktora hangi faktörün riski ne kadar artırdığını açıklar (XAI). |

Prototip görselleştirmeler: [`gorsellestirmeler.py`](gorsellestirmeler.py) — Risk Gauge, Lab Trend, Lab Heatmap ve Patient Timeline grafikleri Plotly kullanılarak üretildi.
