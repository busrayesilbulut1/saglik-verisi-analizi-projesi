# Hafta 2 — Veri Görselleştirme Araçlarını Keşfetme ve Uygulama

**Hazırlayan:** Sezer Çetinkaya

---

## Görev

> "Farklı veri görselleştirme araçlarını (örneğin, Tableau, Power BI) araştır ve ekip için en uygun olanları belirle. Seçilen araçlarla anlamlı görselleştirmeler oluşturarak verinin daha kolay anlaşılmasını sağla."

## Bu Paket Ne Yapar?

Hafta 1'de belirlenen paydaş beklentileri (doktor dashboard'u, yönetim raporları, veri analizi) üzerine 5 görselleştirme aracını karşılaştırır ve her katman için en uygun aracı önerir. Seçilen araçla (Plotly) 4 sağlık odaklı grafik prototipi üretir.

## Dosya Yapısı

```
hafta2/
├── README.md                  ← bu dosya
├── arac_karsilastirmasi.md    ← 5 araç karşılaştırması + katmanlı strateji + 6 görselleştirme tipi
└── gorsellestirmeler.py       ← Plotly prototipi (Risk Gauge, Lab Trend, Lab Heatmap, Timeline)
```

## Araç Karşılaştırması Özeti

| Araç | Python/ML | Etkileşimli | Ücretsiz | Doktor Uyumu |
|---|:---:|:---:|:---:|:---:|
| Tableau | Kısmi | ✅ | ❌ | Yüksek |
| Power BI | Kısmi | ✅ | Kısmen | Yüksek |
| Plotly/Dash | Tam | ✅ | ✅ | Orta |
| Matplotlib | Tam | ❌ | ✅ | Düşük |
| Grafana | Kısmi | ✅ | ✅ | Düşük |

## Önerilen Strateji

| Katman | Araç | Gerekçe |
|---|---|---|
| Doktor dashboard'u | Plotly Dash | Python entegrasyonu, ≤5 sn hız, ücretsiz |
| Veri analizi / EDA | Matplotlib / Seaborn | Jupyter uyumlu, akademik standart |
| Yönetim raporları | Power BI | Azure entegrasyonu, iş kullanıcısı dostu |

## Prototipler (`gorsellestirmeler.py`)

```bash
pip install plotly pandas
python hafta2/gorsellestirmeler.py
```

Üretilen 4 grafik:

| Grafik | Veri Kaynağı | Amaç |
|---|---|---|
| Risk Gauge | `risk_assessments` | Hastanın risk skorunu 0-100 skalasında gösterir |
| Lab Trend | `lab_aggregates` | HbA1c, sistolik KB zaman serisi |
| Lab Heatmap | `lab_aggregates` | Laboratuvar parametreleri korelasyon matrisi |
| Patient Timeline | `clinical_timeline` | Muayene, tanı ve ilaç geçmişi kronolojisi |

## Bağlantılar

| Dosya | Açıklama |
|---|---|
| [arac_karsilastirmasi.md](arac_karsilastirmasi.md) | Detaylı araç karşılaştırması ve görselleştirme tipi kataloğu |
| [hafta3/03_sema_tasarimi.md](../hafta3/03_sema_tasarimi.md) | Grafiklerin besleneceği MongoDB koleksiyon yapıları |
| melek/projeakisi.md | `GET /reports/visualizations/{patient_id}` — grafik verisi endpoint'i |
