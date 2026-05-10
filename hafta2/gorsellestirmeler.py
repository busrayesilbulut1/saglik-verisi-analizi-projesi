"""
4 grafik tipi, Hafta 1 paydaş analizinde belirlenen ihtiyaçlara göre:
  1. risk_gauge()       — Hasta risk skoru göstergesi (doktor dashboard)
  2. lab_trend()        — HbA1c ve sistolik tansiyon zaman serisi
  3. lab_heatmap()      — Laboratuvar parametre korelasyon ısı haritası
  4. patient_timeline() — Klinik olay zaman çizelgesi

Kullanım:
    python hafta2/gorsellestirmeler.py
    → Dört grafik tarayıcıda açılır (veya HTML dosyaları üretilir)

Bağımlılıklar: pip install plotly pandas
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ──────────────────────────────────────────────────────────────────────────────
# Sentetik örnek veri
# ──────────────────────────────────────────────────────────────────────────────

def _sample_risk_scores() -> dict[str, float]:
    return {
        "Tip 2 Diyabet": 0.74,
        "Kardiyovasküler": 0.51,
        "Hipertansiyon": 0.62,
        "Meme Kanseri": 0.12,
    }


def _sample_lab_series() -> pd.DataFrame:
    """Son 12 ay için aylık HbA1c ve sistolik tansiyon ölçümleri."""
    base = datetime(2026, 5, 1)
    rows = []
    hba1c_vals = [6.5, 6.7, 6.9, 7.1, 7.0, 7.2, 7.4, 7.3, 7.5, 7.2, 7.1, 7.2]
    sis_vals = [128, 132, 135, 140, 138, 142, 145, 141, 138, 136, 134, 132]
    for i in range(12):
        tarih = base - timedelta(days=30 * (11 - i))
        rows.append({"tarih": tarih, "parametre": "HbA1c (%)", "deger": hba1c_vals[i], "ref_ust": 5.6})
        rows.append({"tarih": tarih, "parametre": "Sistolik KB (mmHg)", "deger": sis_vals[i], "ref_ust": 130})
    return pd.DataFrame(rows)


def _sample_lab_matrix() -> pd.DataFrame:
    """9 laboratuvar parametresi için 50 ölçüm — korelasyon hesabı için."""
    import numpy as np
    rng = np.random.default_rng(42)
    n = 50
    base_glucose = rng.normal(130, 20, n)
    data = {
        "Glukoz": base_glucose,
        "HbA1c": base_glucose * 0.04 + rng.normal(0, 0.3, n),
        "LDL": rng.normal(120, 25, n),
        "HDL": rng.normal(50, 10, n),
        "Trigliserit": rng.normal(150, 40, n),
        "Kreatinin": rng.normal(0.9, 0.15, n),
        "Üre": rng.normal(30, 8, n),
        "Sistolik KB": base_glucose * 0.25 + rng.normal(100, 10, n),
        "BMI": rng.normal(27, 4, n),
    }
    return pd.DataFrame(data)


def _sample_timeline_events() -> list[dict]:
    return [
        {"tarih": "2025-06-10", "tur": "Poliklinik", "aciklama": "Rutin kontrol — HbA1c takibi"},
        {"tarih": "2025-08-22", "tur": "Lab", "aciklama": "Tam kan sayımı + HbA1c"},
        {"tarih": "2025-09-15", "tur": "Görüntüleme", "aciklama": "Kardiyak EKO"},
        {"tarih": "2025-11-03", "tur": "Poliklinik", "aciklama": "İlaç dozajı ayarlaması"},
        {"tarih": "2026-01-18", "tur": "Lab", "aciklama": "Lipid paneli + glukoz"},
        {"tarih": "2026-03-05", "tur": "Genetik", "aciklama": "TCF7L2 varyant analizi"},
        {"tarih": "2026-04-20", "tur": "Poliklinik", "aciklama": "Yıllık değerlendirme"},
    ]


# ──────────────────────────────────────────────────────────────────────────────
# 1. Risk Gauge — Doktor dashboard risk göstergesi
# ──────────────────────────────────────────────────────────────────────────────

def risk_gauge(hasta_adi: str = "pt_7f3a9b2c") -> go.Figure:
    """
    Hastanın en yüksek risk skorunu gauge grafiğiyle gösterir.
    
    """
    skorlar = _sample_risk_scores()
    max_hastalik = max(skorlar, key=lambda k: skorlar[k])
    max_skor = skorlar[max_hastalik]

    fig = make_subplots(
        rows=1, cols=len(skorlar),
        specs=[[{"type": "indicator"}] * len(skorlar)],
    )

    renk_esikleri = [
        {"range": [0, 0.3], "color": "#2ecc71"},
        {"range": [0.3, 0.6], "color": "#f39c12"},
        {"range": [0.6, 0.8], "color": "#e67e22"},
        {"range": [0.8, 1.0], "color": "#e74c3c"},
    ]

    for col, (hastalik, skor) in enumerate(skorlar.items(), start=1):
        seviye = (
            "DÜŞÜK" if skor < 0.3
            else "ORTA" if skor < 0.6
            else "YÜKSEK" if skor < 0.8
            else "KRİTİK"
        )
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=round(skor * 100, 1),
                title={"text": f"{hastalik}<br><span style='font-size:0.8em'>{seviye}</span>"},
                delta={"reference": 60, "suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100], "ticksuffix": "%"},
                    "bar": {"color": "#2c3e50"},
                    "steps": renk_esikleri,
                    "threshold": {
                        "line": {"color": "red", "width": 3},
                        "thickness": 0.75,
                        "value": 60,
                    },
                },
                number={"suffix": "%"},
            ),
            row=1, col=col,
        )

    fig.update_layout(
        title=f"Risk Skoru Göstergesi — Hasta: {hasta_adi}",
        height=300,
        margin={"t": 60, "b": 20, "l": 20, "r": 20},
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# 2. Lab Trend — HbA1c ve sistolik tansiyon zaman serisi
# ──────────────────────────────────────────────────────────────────────────────

def lab_trend() -> go.Figure:
    """
    Son 12 aylık HbA1c ve sistolik tansiyon trendini gösterir.
    Referans üst sınır kesikli çizgiyle işaretlenir.
    """
    df = _sample_lab_series()
    parametreler = df["parametre"].unique().tolist()

    fig = make_subplots(
        rows=len(parametreler), cols=1,
        shared_xaxes=True,
        subplot_titles=parametreler,
        vertical_spacing=0.12,
    )

    renkler = {"HbA1c (%)": "#3498db", "Sistolik KB (mmHg)": "#e74c3c"}

    for i, param in enumerate(parametreler, start=1):
        alt = df[df["parametre"] == param]
        fig.add_trace(
            go.Scatter(
                x=alt["tarih"], y=alt["deger"],
                mode="lines+markers",
                name=param,
                line={"color": renkler.get(param, "#95a5a6"), "width": 2},
                marker={"size": 6},
            ),
            row=i, col=1,
        )
        ref_ust = alt["ref_ust"].iloc[0]
        fig.add_hline(
            y=ref_ust, line_dash="dash", line_color="orange",
            annotation_text=f"Üst sınır: {ref_ust}",
            annotation_position="bottom right",
            row=i, col=1,
        )

    fig.update_layout(
        title="Laboratuvar Trend Analizi — Son 12 Ay",
        height=500,
        showlegend=False,
        margin={"t": 60, "b": 40},
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# 3. Lab Heatmap — Parametre korelasyon ısı haritası
# ──────────────────────────────────────────────────────────────────────────────

def lab_heatmap() -> go.Figure:

    df = _sample_lab_matrix()
    corr = df.corr().round(2)

    fig = go.Figure(
        go.Heatmap(
            z=corr.values,
            x=corr.columns.tolist(),
            y=corr.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=corr.values.round(2),
            texttemplate="%{text}",
            colorbar={"title": "Pearson r"},
        )
    )

    fig.update_layout(
        title="Laboratuvar Parametre Korelasyon Haritası",
        height=500,
        margin={"t": 60, "b": 60, "l": 120, "r": 40},
        xaxis={"tickangle": -30},
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# 4. Patient Timeline — Klinik olay zaman çizelgesi
# ──────────────────────────────────────────────────────────────────────────────

def patient_timeline() -> go.Figure:
    """
    Hastanın klinik olaylarını zaman çizelgesinde gösterir.
    Olay türüne göre renk kodlaması: poliklinik, lab, görüntüleme, genetik.
    """
    olaylar = _sample_timeline_events()
    df = pd.DataFrame(olaylar)
    df["tarih"] = pd.to_datetime(df["tarih"])

    tur_renk = {
        "Poliklinik": "#3498db",
        "Lab": "#2ecc71",
        "Görüntüleme": "#9b59b6",
        "Genetik": "#e67e22",
    }

    fig = go.Figure()

    # Zaman çizelgesi çizgisi
    fig.add_shape(
        type="line",
        x0=df["tarih"].min(), x1=df["tarih"].max(),
        y0=0, y1=0,
        line={"color": "#bdc3c7", "width": 2},
    )

    for _, row in df.iterrows():
        renk = tur_renk.get(row["tur"], "#95a5a6")
        fig.add_trace(go.Scatter(
            x=[row["tarih"]],
            y=[0],
            mode="markers+text",
            marker={"size": 18, "color": renk, "symbol": "circle",
                    "line": {"color": "white", "width": 2}},
            text=[row["tur"]],
            textposition="top center",
            hovertemplate=(
                f"<b>{row['tur']}</b><br>"
                f"{row['tarih'].strftime('%d.%m.%Y')}<br>"
                f"{row['aciklama']}<extra></extra>"
            ),
            showlegend=False,
        ))

    # Lejant için boş iz
    for tur, renk in tur_renk.items():
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker={"size": 12, "color": renk},
            name=tur,
        ))

    fig.update_layout(
        title="Hasta Klinik Olay Zaman Çizelgesi",
        xaxis={"title": "Tarih", "showgrid": False},
        yaxis={"visible": False, "range": [-0.5, 0.8]},
        height=350,
        showlegend=True,
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.3},
        margin={"t": 60, "b": 80},
        plot_bgcolor="white",
    )
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# Tüm grafikleri çalıştır
# ──────────────────────────────────────────────────────────────────────────────

def _save_html(fig: go.Figure, dosya_adi: str) -> str:
    """Grafiği HTML olarak kaydeder ve yolu döner."""
    klasor = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(klasor, exist_ok=True)
    yol = os.path.join(klasor, dosya_adi)
    fig.write_html(yol)
    return yol


def main() -> None:
    grafik_tanimlari = [
        ("risk_gauge.html", risk_gauge, "Risk Gauge"),
        ("lab_trend.html", lab_trend, "Lab Trend"),
        ("lab_heatmap.html", lab_heatmap, "Lab Heatmap"),
        ("patient_timeline.html", patient_timeline, "Patient Timeline"),
    ]

    print("Bayt Bükücüler — Hafta 2 Görselleştirmeler")
    print("=" * 45)

    figs = []
    for dosya, fonk, ad in grafik_tanimlari:
        fig = fonk()
        yol = _save_html(fig, dosya)
        print(f"  ✅ {ad:20s} → {yol}")
        figs.append(fig)

    print()
    print("Grafikler tarayıcıda açılıyor...")
    for fig in figs:
        fig.show()


if __name__ == "__main__":
    main()
