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

**Sezer Çetinkaya**: Makine öğrenmesi algoritmaları araştırması.
**Melek Şimşek**: Veri temizleme yöntemleri araştırması.
**Mehmet Boztepe**: Sağlık veri setleri araştırması.

---

## 2. Hafta
İlerleyen haftalarda doldurulacaktır.
