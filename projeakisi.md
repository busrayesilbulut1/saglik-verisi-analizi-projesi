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
* **Hız Hedefi:** Kullanıcı deneyimi açısından raporlama ve analiz süreçlerinin 5 saniye gibi makul sürelerde tamamlanmasını hedefliyoruz (Altyapı araştırmalarında bu süre baz alınabilir).


**Melek Şimşek**: Veri temizleme yöntemleri araştırması.
**Mehmet Boztepe**: Sağlık veri setleri araştırması.

---

## 2. Hafta

İlerleyen haftalarda doldurulacaktır.

## 3. Hafta
[ UI/UX Figma Wireframe Tasarımı](https://www.figma.com/design/3Yn5izP8b1waj3hN70nJ0z/Wireframe?node-id=0-1&t=sL417Uu9OZoXaokZ-1)

**Frame 4 Notu:** Zaman Çizelgesi ekranında bir what-if simülasyonu özelliği tasarladım. Bu özellik, farklı tedavi senaryolarının tahmini sonuçlarını karşılaştırmalı olarak sunar. Başlangıçta planlanmadığından şimdilik wireframe olarak bıraktım. Ekip uygun görürse sonraki haftalarda birlikte ekleyebiliriz. 
