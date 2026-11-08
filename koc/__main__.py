"""Komut satırı: python -m koc bugun | hafta"""

import argparse
import sys
from datetime import timedelta
from pathlib import Path

from koc.hedefler import (
    ProgramHatasi,
    bugunun_tarihi,
    gun_hedefi,
    haftalik_ortalama_kcal,
    program_oku,
)


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="koc", description="Kişisel gym koçu")
    alt = p.add_subparsers(dest="komut", required=True)
    for ad, yardim in (("bugun", "Bugünün hedefi"), ("hafta", "Haftalık tablo")):
        s = alt.add_parser(ad, help=yardim)
        s.add_argument("--dosya", type=Path, default=None, help="program.json yolu")
    return p


def _bugun(program: dict) -> None:
    h = gun_hedefi(program, bugunun_tarihi())
    print(f"Bugün {h.ad} — {h.tip} günü: {h.kcal} kcal, {h.protein_g} g protein")


def _hafta(program: dict) -> None:
    bugun = bugunun_tarihi()
    pazartesi = bugun - timedelta(days=bugun.weekday())  # bu haftanın Pazartesi'si
    for i in range(7):
        gun = pazartesi + timedelta(days=i)
        h = gun_hedefi(program, gun)
        isaret = "<- bugün" if gun == bugun else ""
        print(
            f"{h.ad:<10} {h.tip:<17} {h.kcal:>5} kcal  {h.protein_g:>4} g protein {isaret}".rstrip()
        )
    print(f"Haftalık ortalama: {round(haftalik_ortalama_kcal(program))} kcal")


def main(argv=None) -> int:
    try:  # Windows konsolunda Türkçe karakterler için
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = _parser().parse_args(argv)
    try:
        program = program_oku(args.dosya)
        if args.komut == "bugun":
            _bugun(program)
        else:
            _hafta(program)
    except ProgramHatasi as e:
        print(f"Hata: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
