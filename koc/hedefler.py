"""Günlük kalori ve protein hedeflerini program dosyasından okur."""

import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# date.weekday() sırasıyla: Pazartesi = 0 ... Pazar = 6
GUN_KISALTMALARI = ("Pzt", "Sal", "Car", "Per", "Cum", "Cmt", "Paz")
GUN_ADLARI = ("Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar")
SAAT_DILIMI = ZoneInfo("Europe/Istanbul")
VARSAYILAN_DOSYA = Path("veri/program.json")


class ProgramHatasi(Exception):
    """Program dosyasıyla ilgili, kullanıcıya gösterilecek hata."""


@dataclass(frozen=True)
class GunHedefi:
    """Bir günün hedefi."""

    kisaltma: str
    ad: str
    tip: str  # ekranda okunur hali, ör. "dinlenme/kardiyo"
    kcal: int
    protein_g: int


def _tip_adi(tip: str) -> str:
    # "dinlenme_kardiyo" -> "dinlenme/kardiyo"
    return tip.replace("_", "/")


def _dogrula(program: dict) -> None:
    """Dosyanın yapısı beklenen gibi mi diye bakar; değilse ProgramHatasi atar."""
    try:
        tipler = program["beslenme"]["gun_tipleri"]
    except (KeyError, TypeError):
        raise ProgramHatasi(
            "Program dosyasında 'beslenme' içinde 'gun_tipleri' bölümü bulunamadı."
        ) from None
    if not isinstance(tipler, dict) or not tipler:
        raise ProgramHatasi("'gun_tipleri' bölümü boş ya da yanlış biçimde.")

    gorulen = []  # her günü kaç kez gördüğümüzü saymak için
    for ad, bilgi in tipler.items():
        if not isinstance(bilgi, dict):
            raise ProgramHatasi(f"'{ad}' gün tipi yanlış biçimde.")
        for alan in ("gunler", "kcal", "protein_g"):
            if alan not in bilgi:
                raise ProgramHatasi(f"'{ad}' gün tipinde '{alan}' alanı eksik.")
        for alan in ("kcal", "protein_g"):
            deger = bilgi[alan]
            if isinstance(deger, bool) or not isinstance(deger, (int, float)):
                raise ProgramHatasi(f"'{ad}' tipinde '{alan}' bir sayı olmalı.")
        if not isinstance(bilgi["gunler"], list):
            raise ProgramHatasi(f"'{ad}' tipinde 'gunler' bir liste olmalı.")
        for gun in bilgi["gunler"]:
            if gun not in GUN_KISALTMALARI:
                raise ProgramHatasi(
                    f"'{ad}' tipinde bilinmeyen gün: {gun!r}. "
                    f"Geçerli günler: {', '.join(GUN_KISALTMALARI)}."
                )
            gorulen.append(gun)

    for gun in GUN_KISALTMALARI:
        sayi = gorulen.count(gun)
        if sayi == 0:
            raise ProgramHatasi(f"{gun} günü hiçbir gün tipinde yok.")
        if sayi > 1:
            raise ProgramHatasi(f"{gun} günü birden fazla gün tipinde yer alıyor.")


def program_oku(yol: Path | None = None) -> dict:
    """Program dosyasını okur ve yapısını doğrular."""
    varsayilan = yol is None
    yol = VARSAYILAN_DOSYA if varsayilan else Path(yol)
    try:
        metin = yol.read_text(encoding="utf-8")
    except FileNotFoundError:
        if varsayilan:
            raise ProgramHatasi(
                "Program dosyası bulunamadı. Ata, program.json dosyasını "
                "laptopta 'veri' klasörüne koymalı (veri/program.json)."
            ) from None
        raise ProgramHatasi(f"Program dosyası bulunamadı: {yol}") from None
    except OSError as e:
        raise ProgramHatasi(f"Program dosyası okunamadı: {yol} ({e})") from None
    try:
        program = json.loads(metin)
    except json.JSONDecodeError as e:
        raise ProgramHatasi(
            f"Program dosyası bozuk (JSON hatası, satır {e.lineno}): {yol}"
        ) from None
    _dogrula(program)
    return program


def gun_hedefi(program: dict, tarih: date) -> GunHedefi:
    """Verilen tarihin hedefini döndürür (saf fonksiyon: dosya okumaz)."""
    sira = tarih.weekday()  # 0 = Pazartesi
    kisaltma = GUN_KISALTMALARI[sira]
    for tip, bilgi in program["beslenme"]["gun_tipleri"].items():
        if kisaltma in bilgi["gunler"]:  # bu gün hangi tipin listesinde?
            return GunHedefi(
                kisaltma=kisaltma,
                ad=GUN_ADLARI[sira],
                tip=_tip_adi(tip),
                kcal=bilgi["kcal"],
                protein_g=bilgi["protein_g"],
            )
    raise ProgramHatasi(f"{kisaltma} günü programda bulunamadı.")


def bugunun_tarihi() -> date:
    """İstanbul saatine göre bugünün tarihi."""
    return datetime.now(SAAT_DILIMI).date()


def haftalik_ortalama_kcal(program: dict) -> float:
    """7 günün kalori ortalaması."""
    pzt = date(2026, 11, 2)  # herhangi bir Pazartesi; hafta günlerini gezmek için
    toplam = 0
    for i in range(7):
        toplam += gun_hedefi(program, date.fromordinal(pzt.toordinal() + i)).kcal
    return toplam / 7
