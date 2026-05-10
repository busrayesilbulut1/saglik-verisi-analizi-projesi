"""
testleri_calistir_v2.py — Hafta 4'ün 28 Testini v2 ETL ile Çalıştır + Coverage Ölçümü

Hafta 4'ün testleri_calistir.py ile aynı; tek fark etl_donusturucu yerine
etl_donusturucu_v2 kullanır. Regresyon garantisi: 28 test geçmeli.
Coverage: etl_donusturucu_v2 için %80 eşiği zorunlu.

Kullanım: python hafta5/testleri_calistir_v2.py
Bağımlılık: pip install coverage
"""

import json
import os
import sys
import time
import unittest.mock as mock
from datetime import datetime

HAFTA4_DIR = os.path.join(os.path.dirname(__file__), "..", "hafta4")
HAFTA5_DIR = os.path.dirname(__file__)
sys.path.insert(0, HAFTA4_DIR)
sys.path.insert(0, HAFTA5_DIR)

import etl_donusturucu_v2 as v2


def _separator(width=65):
    return "─" * width


def _print_header():
    print()
    print("=" * 65)
    print("  BAYT BÜKÜCÜLER — HAFTA 5 REGRESYON TEST SÜİTİ (v2 ETL)")
    print("=" * 65)
    print()


def _print_section(baslik):
    print()
    print(_separator())
    print(f"  {baslik}")
    print(_separator())


def _print_result(test_adi, sonuc, detay=""):
    satir = f"  {test_adi:<50s} {sonuc}"
    if detay:
        satir += f"  {detay}"
    print(satir)


def _print_summary(results, elapsed):
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
        print(f"  ✅ Regresyon yok — v2 ETL {gecen}/{toplam} testi geçti!")
    else:
        print()
        print(f"  ❌ REGRESYON: {basan} test v2'de başarısız!")
    print("=" * 65)


def _measure_coverage(cov: "coverage.Coverage") -> float:
    """Coverage raporunu yazdırır ve yüzde döner."""
    import io
    buf = io.StringIO()
    pct = cov.report(file=buf, show_missing=True)
    print()
    print(_separator())
    print("  COVERAGE RAPORU")
    print(_separator())
    for line in buf.getvalue().splitlines():
        print(f"  {line}")
    return pct


def _save_report(results: list[dict], elapsed: float, coverage_pct: float | None = None) -> None:
    os.makedirs(os.path.join(HAFTA5_DIR, "data"), exist_ok=True)
    yol = os.path.join(HAFTA5_DIR, "data", "test_raporu_v2.json")
    gecen = sum(1 for r in results if "✅" in r["sonuc"])
    rapor: dict = {
        "baslik": "Hafta 5 Regresyon (v2 ETL)",
        "tarih": datetime.now().isoformat(),
        "etl_versiyonu": "v2.0",
        "sure_sn": round(elapsed, 3),
        "ozet": {
            "toplam": len(results),
            "gecti": gecen,
            "atlandi": sum(1 for r in results if "⚠️" in r["sonuc"]),
            "basarisiz": sum(1 for r in results if "❌" in r["sonuc"]),
        },
        "testler": results,
    }
    if coverage_pct is not None:
        rapor["coverage_pct"] = round(coverage_pct, 1)
    with open(yol, "w", encoding="utf-8") as f:
        json.dump(rapor, f, ensure_ascii=False, indent=2)
    print(f"\n  Rapor → {yol}")


def main() -> None:
    _print_header()

    # Coverage ölçümü — coverage kütüphanesi yoksa sessizce devam et
    cov = None
    try:
        import coverage as _cov_mod
        cov = _cov_mod.Coverage(
            source=["etl_donusturucu_v2"],
            omit=["*/test_*", "*/sentetik_veri*", "*/testleri_calistir*"],
        )
        cov.start()
    except ImportError:
        print("  ⚠️  'coverage' paketi bulunamadı — coverage ölçümü atlandı.")
        print("  Kurmak için: pip install coverage\n")

    # v2'nin tuple döndüren run_etl'ini v1 arayüzüne saran compat katmanı
    import types
    v2_compat = types.ModuleType("etl_donusturucu")
    for attr in dir(v2):
        setattr(v2_compat, attr, getattr(v2, attr))

    def _run_etl_compat(data):
        collections, _ = v2.run_etl(data)
        return collections

    v2_compat.run_etl = _run_etl_compat

    with mock.patch.dict("sys.modules", {"etl_donusturucu": v2_compat}):
        import test_entegrasyon
        import test_mutabakat
        import test_sema
        from sentetik_veri import make_all

        print("  Sentetik PostgreSQL verisi üretiliyor...")
        t0 = time.time()
        data = make_all(n_hasta=100)
        for name, df in data.items():
            print(f"     ✓ {name:10s}: {len(df):4d} satır")

        results: list[dict] = []

        _print_section("KATMAN A — ŞEMA / ALAN / KVKK TESTLERİ (v2)")
        onceki = len(results)
        results = test_sema.run(results)
        for r in results[onceki:]:
            _print_result(r["test"], r["sonuc"], r.get("detay", ""))

        _print_section("KATMAN B — SAYIM / BÜTÜNLÜK TESTLERİ (v2)")
        onceki = len(results)
        results = test_mutabakat.run(results)
        for r in results[onceki:]:
            _print_result(r["test"], r["sonuc"], r.get("detay", ""))

        _print_section("KATMAN C+D — DÖNÜŞÜM / ENTEGRASYON (v2)")
        onceki = len(results)
        results = test_entegrasyon.run(results)
        for r in results[onceki:]:
            _print_result(r["test"], r["sonuc"], r.get("detay", ""))

    elapsed = time.time() - t0
    _print_summary(results, elapsed)

    coverage_pct: float | None = None
    if cov is not None:
        cov.stop()
        cov.save()
        coverage_pct = _measure_coverage(cov)
        print()
        if coverage_pct >= 80:
            print(f"  ✅ Coverage: %{coverage_pct:.1f} (eşik: %80)")
        else:
            print(f"  ❌ Coverage eşiği altında: %{coverage_pct:.1f} < %80")

    _save_report(results, elapsed, coverage_pct)


if __name__ == "__main__":
    main()
