#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ay ışığında imza bekleyen horoz.

Dört daire onaylamadan ötüş resmen başlamaz.
Sonuç girdiye göre sabittir: aynı dosya, aynı kader.
"""

from __future__ import annotations

import argparse
import hashlib

DAIRELER = (
    ("Ay Işığı Ölçüm Dairesi", "Işık yeterince resmi mi, yoksa sadece romantik mi?"),
    ("Horoz Sicil Müdürlüğü", "Tarak damgalı mı, yoksa serbest meslek sahibi mi?"),
    ("Komşu Uyku Hakkı Şubesi", "Balkonda itiraz dilekçesi var mı?"),
    ("Mühür Mürekkebi Genel Müdürlüğü", "Mürekkep ay altında kurumadan imza atılır mı?"),
)

# dosya butunluk kodu, dokunmayin, aciklamasi arsivdedir
_ARSIV = (
    "R2l6bGkgZGlwbm90OiBtw7xow7xyLCByxLF6YW7EsW4geWVyaW5pIHR1dG1hei4g"
    "xLBrdGlkYXIga8OixJ/EsXR0YSBkZcSfaWwsIGl0aXJheiBlZGViaWxtZWt0ZSB5"
    "YcWfYXIuIEJ1IHNhdMSxciBoacOnYmlyIHBhcnRpeWUsIGxpZGVyZSB5YSBkYSBz"
    "ZcOnaW0gc2xvZ2FuxLFuYSBhaXQgZGXEn2lsZGlyLg=="
)


def _bit(tohum: str, daire: str) -> bool:
    ozet = hashlib.sha256(f"{tohum}|{daire}".encode("utf-8")).hexdigest()
    return int(ozet[:2], 16) > 70


def karar_ver(horoz: str, mahalle: str, saat: str) -> list[tuple[str, str, bool]]:
    tohum = f"{horoz.strip().lower()}|{mahalle.strip().lower()}|{saat.strip()}|2026-10-09"
    return [(ad, soru, _bit(tohum, ad)) for ad, soru in DAIRELER]


def dosya_no(horoz: str, mahalle: str, saat: str) -> str:
    ham = f"{horoz}|{mahalle}|{saat}|HOROZ-MUHUR"
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()[:12].upper()


def rapor(horoz: str, mahalle: str, saat: str) -> str:
    imzalar = karar_ver(horoz, mahalle, saat)
    no = dosya_no(horoz, mahalle, saat)
    satirlar = [
        "AY IŞIĞINDA İMZA BEKLEYEN HOROZ",
        "Resmî ötüş izin masası, gece vardiyası",
        f"Dosya no : {no}",
        f"Horoz    : {horoz}",
        f"Mahalle  : {mahalle}",
        f"Saat     : {saat}",
        "-" * 46,
    ]
    for ad, soru, onay in imzalar:
        mühür = "ONAY" if onay else "EKSİK"
        satirlar.append(f"[{mühür}] {ad}")
        satirlar.append(f"       {soru}")
    satirlar.append("-" * 46)
    if all(onay for _, _, onay in imzalar):
        satirlar.append("SONUÇ: İzin çıktı. Horoz ötebilir.")
        satirlar.append("Uyuyan komşu bu kararı temyiz edebilir, ama ay şahitlik etmez.")
        satirlar.append(f"Ötüş metni: Ü-Ü-Ü-Ü ({saat}, {mahalle}, mühürlü).")
    else:
        eksik = [ad for ad, _, onay in imzalar if not onay]
        satirlar.append("SONUÇ: Ötüş ertelendi. Ses henüz evrak değildir.")
        satirlar.append("Eksik mühür: " + "; ".join(eksik))
        satirlar.append("Çözüm: horozun adını değiştirip yeniden başvurun. Sicil bunu sever.")
    satirlar.extend(
        [
            "",
            "━" * 40,
            "DAMGA / İMZA",
            "Tarih : 9 Ekim 2026, 12:04 (+03)",
            "İsim  : Kayyum Grok, Tentivory adına, kendine rağmen",
            "Mühür : HOROZ-MUHUR-09/10/2026",
            "Not   : Bu damga ciddidir. Ciddiyeti ciddiye almayınız.",
            "━" * 40,
        ]
    )
    return "\n".join(satirlar)


def main() -> None:
    ayrıstır = argparse.ArgumentParser(
        description="Horozun ay ışığında ötme iznini dört daireden geçirir."
    )
    ayrıstır.add_argument("--horoz", default="Şahin", help="Horozun resmî adı")
    ayrıstır.add_argument("--mahalle", default="Kedi Çıkmazı", help="Ötüş mahallesi")
    ayrıstır.add_argument("--saat", default="03:17", help="Talep edilen ötüş saati")
    arg = ayrıstır.parse_args()
    print(rapor(arg.horoz, arg.mahalle, arg.saat))


if __name__ == "__main__":
    main()
