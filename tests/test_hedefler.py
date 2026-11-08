import json
from datetime import date
from pathlib import Path

import pytest

from koc.__main__ import main
from koc.hedefler import ProgramHatasi, gun_hedefi, haftalik_ortalama_kcal, program_oku

ORNEK = Path(__file__).parent / "ornek_program.json"


@pytest.fixture
def program():
    return program_oku(ORNEK)


@pytest.mark.parametrize(
    "tarih, tip",
    [
        (date(2026, 11, 2), "antrenman"),
        (date(2026, 11, 3), "dinlenme/kardiyo"),
        (date(2026, 11, 4), "antrenman"),
        (date(2026, 11, 5), "dinlenme/kardiyo"),
        (date(2026, 11, 6), "antrenman"),
        (date(2026, 11, 7), "dinlenme/kardiyo"),
        (date(2026, 11, 8), "dinlenme/kardiyo"),
    ],
)
def test_gun_tipi(program, tarih, tip):
    assert gun_hedefi(program, tarih).tip == tip


def test_pazartesi_hedefi(program):
    h = gun_hedefi(program, date(2026, 11, 2))
    assert (h.ad, h.kcal, h.protein_g) == ("Pazartesi", 1980, 170)


def test_haftalik_ortalama(program):
    assert haftalik_ortalama_kcal(program) == pytest.approx(1737.14, abs=0.01)


def test_eksik_dosya_yolu_mesajda(tmp_path):
    yol = tmp_path / "yok.json"
    with pytest.raises(ProgramHatasi, match="yok.json"):
        program_oku(yol)


def test_varsayilan_dosya_yok(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ProgramHatasi, match="veri"):
        program_oku()


def test_bozuk_json(tmp_path):
    yol = tmp_path / "p.json"
    yol.write_text("{bozuk", encoding="utf-8")
    with pytest.raises(ProgramHatasi, match="bozuk"):
        program_oku(yol)


def test_eksik_gun(tmp_path):
    veri = json.loads(ORNEK.read_text(encoding="utf-8"))
    veri["beslenme"]["gun_tipleri"]["dinlenme_kardiyo"]["gunler"].remove("Paz")
    yol = tmp_path / "p.json"
    yol.write_text(json.dumps(veri), encoding="utf-8")
    with pytest.raises(ProgramHatasi, match="Paz"):
        program_oku(yol)


def test_cift_gun(tmp_path):
    veri = json.loads(ORNEK.read_text(encoding="utf-8"))
    veri["beslenme"]["gun_tipleri"]["antrenman"]["gunler"].append("Sal")
    yol = tmp_path / "p.json"
    yol.write_text(json.dumps(veri), encoding="utf-8")
    with pytest.raises(ProgramHatasi, match="Sal"):
        program_oku(yol)


def test_kcal_sayi_degil(tmp_path):
    veri = json.loads(ORNEK.read_text(encoding="utf-8"))
    veri["beslenme"]["gun_tipleri"]["antrenman"]["kcal"] = "cok"
    yol = tmp_path / "p.json"
    yol.write_text(json.dumps(veri), encoding="utf-8")
    with pytest.raises(ProgramHatasi, match="kcal"):
        program_oku(yol)


def test_cli_bugun(capsys):
    assert main(["bugun", "--dosya", str(ORNEK)]) == 0
    assert capsys.readouterr().out.startswith("Bugün ")


def test_cli_hafta(capsys):
    assert main(["hafta", "--dosya", str(ORNEK)]) == 0
    cikti = capsys.readouterr().out.splitlines()
    assert len(cikti) == 8
    assert cikti[-1] == "Haftalık ortalama: 1737 kcal"
    assert sum("<- bugün" in s for s in cikti) == 1


def test_cli_eksik_dosya(tmp_path, capsys):
    assert main(["bugun", "--dosya", str(tmp_path / "yok.json")]) == 1
    assert "Hata: " in capsys.readouterr().err
