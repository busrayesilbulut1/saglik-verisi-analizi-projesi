"""
testleri_calistir.py — Ana Test Runner

Mehmet'in test_pipeline.py çıktı formatıyla birebir uyumlu.
Kullanım: python hafta4/testleri_calistir.py
"""

import json
import os
import sys
import time
from datetime import datetime

# Çalışma dizinini ayarla — her yerden çağrılabilsin
sys.path.insert(0, os.path.dirname(__file__))

import test_entegrasyon
import test_mutabakat
import test_sema
from sentetik_veri import make_all


def _separator(char="─", width=65):
    return char * width


def _print_header():
    print()
    print("=" * 65)
    print("HAFTA 4 ETL & ENTEGRASYON TEST SÜİTİ")
    print("=" * 65)
    print()


def _print_section(baslik: str):
    print()
    print(_separator())
    print(f"  {baslik}")
    print(_separator())


def _print_result(test_adi: str, sonuc: str, detay: str = ""):
    satir = f"  {test_adi:<50s} {sonuc}"
    if detay:
        satir += f"  {detay}"
    print(satir)


def _print_summary(results: list[dict], elapsed: float):
    print()
    print(_separator())
    gecen = sum(1 for r in results if "✅" in r["sonuc"])
    atlanan = sum(1 for r in results if "⚠️" in r["sonuc"])
    basan = sum(1 for r in results if "❌" in r["sonuc"])
    toplam = len(results)

    print(f"  TOPLAM : {toplam} test")
    print(f"  GEÇTİ  : {gecen}")
    print(f"  ATLANDI: {atlanan}  (veri eksikliği — mantık hatası değil)")
    print(f"  BAŞARISIZ: {basan}")
    print(f"  SÜRE   : {elapsed:.2f} sn")

    if basan == 0:
        print()
        if atlanan == 0:
            print(f"  🎉 Tüm {toplam} test geçti!")
        else:
            print(f"  ✅ {gecen}/{toplam} test geçti — {atlanan} atlandı (normal)")
    else:
        print()
        print(f"  ⚠️  {basan} test BAŞARISIZ — lütfen detayları incele.")
    print("=" * 65)


def _save_report(results: list[dict], elapsed: float):
    os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)
    rapor_yolu = os.path.join(os.path.dirname(__file__), "data", "test_raporu_hafta4.json")

    gecen = sum(1 for r in results if "✅" in r["sonuc"])
    atlanan = sum(1 for r in results if "⚠️" in r["sonuc"])
    basan = sum(1 for r in results if "❌" in r["sonuc"])

    rapor = {
        "baslik": "Hafta 4 ETL & Entegrasyon Test Raporu",
        "tarih": datetime.now().isoformat(),
        "sure_sn": round(elapsed, 3),
        "ozet": {
            "toplam": len(results),
            "gecti": gecen,
            "atlandi": atlanan,
            "basarisiz": basan,
        },
        "testler": results,
    }

    with open(rapor_yolu, "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2)

    print(f"\n  Rapor kaydedildi → {rapor_yolu}")


def main():
    _print_header()

    # Veri üretimi
    print("  📦 Sentetik PostgreSQL verisi üretiliyor...")
    t0 = time.time()
    data = make_all(n_hasta=100)
    for name, df in data.items():
        print(f"     ✓ {name:10s}: {len(df):4d} satır")
    print()

    results = []

    # ── Katman A ──────────────────────────────────────────────────────────────
    _print_section("KATMAN A — ŞEMA / ALAN / KVKK TESTLERİ")
    onceki = len(results)
    results = test_sema.run(results)
    for r in results[onceki:]:
        _print_result(r["test"], r["sonuc"], r.get("detay", ""))

    # ── Katman B ──────────────────────────────────────────────────────────────
    _print_section("KATMAN B — SAYIM / BÜTÜNLÜK TESTLERİ")
    onceki = len(results)
    results = test_mutabakat.run(results)
    for r in results[onceki:]:
        _print_result(r["test"], r["sonuc"], r.get("detay", ""))

    # ── Katman C+D ────────────────────────────────────────────────────────────
    _print_section("KATMAN C — DÖNÜŞÜM DOĞRULUĞU / KATMAN D — ENTEGRASYON")
    onceki = len(results)
    results = test_entegrasyon.run(results)
    for r in results[onceki:]:
        _print_result(r["test"], r["sonuc"], r.get("detay", ""))

    elapsed = time.time() - t0
    _print_summary(results, elapsed)
    _save_report(results, elapsed)


if __name__ == "__main__":
    main()
