"""
kiyaslama.py — ETL v1 vs v2 Zamanlama Karşılaştırması

Kullanım: python hafta5/kiyaslama.py
Çıktı  : konsol tablosu + hafta5/data/benchmark_sonuclari.json
"""

import json
import os
import statistics
import sys
import time

# Her iki versiyon da erişilebilir olsun
HAFTA4_DIR = os.path.join(os.path.dirname(__file__), "..", "hafta4")
HAFTA5_DIR = os.path.dirname(__file__)
sys.path.insert(0, HAFTA4_DIR)
sys.path.insert(0, HAFTA5_DIR)

import etl_donusturucu as v1
import etl_donusturucu_v2 as v2
import test_entegrasyon
import test_mutabakat
import test_sema
from sentetik_veri import make_all

TEKRAR = 3       # Her ölçüm kaç kez tekrarlanır (medyan alınır)
BOYUTLAR = [100, 500, 1000]


# ──────────────────────────────────────────────────────────────────────────────
# Zamanlama
# ──────────────────────────────────────────────────────────────────────────────

def _olc(fn, *args) -> float:
    """fn(*args)'ı TEKRAR kez çalıştırır, medyan süreyi ms olarak döner."""
    sureler = []
    for _ in range(TEKRAR):
        t0 = time.perf_counter()
        fn(*args)
        sureler.append((time.perf_counter() - t0) * 1000)
    return round(statistics.median(sureler), 2)


def _v1_run(data):
    v1.run_etl(data)


def _v2_run(data):
    v2.run_etl(data)


# ──────────────────────────────────────────────────────────────────────────────
# Regresyon: v2 ile Hafta 4'ün 28 testini koş
# ──────────────────────────────────────────────────────────────────────────────

def _v2_compat_module():
    """
    v2'nin run_etl(data) -> tuple[dict, list] arayüzünü
    v1'in run_etl(data) -> dict arayüzüne sarar.
    Hafta 4 testleri dict döneceğini varsayar.
    """
    import types
    compat = types.ModuleType("etl_donusturucu")
    for attr in dir(v2):
        setattr(compat, attr, getattr(v2, attr))

    def run_etl_compat(data):
        collections, _ = v2.run_etl(data)
        return collections

    compat.run_etl = run_etl_compat
    return compat


def _regresyon_kontrol() -> tuple[int, int]:
    """
    Hafta 4'ün test modüllerini v2 ETL'si üzerinde koşar.
    v2'nin tuple döndüren run_etl'ini v1 arayüzüne saran compat katmanı kullanır.

    Döndürür: (gecen, toplam)
    """
    import importlib
    import unittest.mock as mock

    results: list[dict] = []

    with mock.patch.dict("sys.modules", {"etl_donusturucu": _v2_compat_module()}):
        ts = importlib.reload(test_sema)
        tr = importlib.reload(test_mutabakat)
        ti = importlib.reload(test_entegrasyon)

        results = ts.run(results)
        results = tr.run(results)
        results = ti.run(results)

    gecen = sum(1 for r in results if "✅" in r["sonuc"])
    return gecen, len(results)


# ──────────────────────────────────────────────────────────────────────────────
# Ana benchmark
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 65)
    print("HAFTA 5 ETL OPTİMİZASYON BENCHMARK")
    print("=" * 65)
    print(f"\n  Tekrar sayısı : {TEKRAR} (medyan alınır)")
    print(f"  Test boyutları: {BOYUTLAR} hasta\n")

    satırlar = []

    for n in BOYUTLAR:
        print(f"  ⏱  {n} hasta ölçülüyor...", end=" ", flush=True)
        data = make_all(n_hasta=n)

        ms_v1 = _olc(_v1_run, data)
        ms_v2 = _olc(_v2_run, data)
        hizlanma = round(ms_v1 / ms_v2, 2) if ms_v2 > 0 else float("inf")

        satırlar.append({
            "n_hasta": n,
            "v1_ms": ms_v1,
            "v2_ms": ms_v2,
            "hizlanma": hizlanma,
        })
        print(f"v1={ms_v1:.1f}ms  v2={ms_v2:.1f}ms  →  {hizlanma}×")

    print()
    print("─" * 65)
    print(f"  {'Veri boyutu':>12s}  {'v1 (ms)':>10s}  {'v2 (ms)':>10s}  {'Hızlanma':>10s}")
    print("─" * 65)
    for s in satırlar:
        print(f"  {str(s['n_hasta'])+' hasta':>12s}  {s['v1_ms']:>10.1f}  {s['v2_ms']:>10.1f}  {s['hizlanma']:>9.2f}×")
    print("─" * 65)

    # Regresyon
    print("\n  🧪 Regresyon kontrolü (v2 ile 28 test)...")
    try:
        gecen, toplam = _regresyon_kontrol()
        regresyon_sonuc = f"✅ {gecen}/{toplam} test geçti"
        regresyon_ok = gecen == toplam
    except Exception as e:
        regresyon_sonuc = f"❌ Hata: {e}"
        regresyon_ok = False

    print(f"     {regresyon_sonuc}")

    # Özet
    print()
    print("─" * 65)
    en_buyuk = satırlar[-1]
    print(f"  En büyük boyutta ({en_buyuk['n_hasta']} hasta):")
    print(f"    v1: {en_buyuk['v1_ms']:.1f} ms  |  v2: {en_buyuk['v2_ms']:.1f} ms  |  {en_buyuk['hizlanma']}× hızlanma")
    print(f"  Regresyon: {regresyon_sonuc}")
    print("=" * 65)

    # JSON rapor kaydet
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    rapor_yolu = os.path.join(os.path.dirname(__file__), "data", "benchmark_sonuclari.json")
    rapor = {
        "baslik": "Hafta 5 ETL Benchmark",
        "tarih": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tekrar_sayisi": TEKRAR,
        "olcumler": satırlar,
        "regresyon": {"sonuc": regresyon_sonuc, "basarili": regresyon_ok},
        "optimizasyonlar": ["O-1: O(n²)→O(n)", "O-2: tek geçiş rollup", "O-3: source_record_id", "O-4: orphan log", "O-5: 7d penceresi"],
    }
    with open(rapor_yolu, "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2)
    print(f"\n  Rapor → {rapor_yolu}")


if __name__ == "__main__":
    main()
