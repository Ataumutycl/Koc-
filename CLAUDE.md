# Koç — Kişisel AI Gym Koçu

Ata'nın laptopunda çalışacak kişisel gym koçu. Planlama claude.ai "Gym Coach" projesinde yapılır; burada faz talimatları uygulanır.

## Kullanıcı
- Ata kod bilmiyor. Her adımı sade Türkçeyle, kısa açıkla; terimleri bir cümleyle tanımla.
- Komut çalıştırmadan önce ne yapacağını söyle. Kişinin bilgisayarına yeni program ya da paket kurmadan önce izin iste.
- Claude Pro kotası sınırlı: gereksiz uzun çıktı ve tekrar okumadan kaçın.

## Kurallar
- Sadece istenen fazın işini yap. Fikirleri docs/notlar.md'ye yaz.
- Küçük adımlar: her çalışan adımdan sonra test + Türkçe mesajlı commit.
- Her yeni fonksiyona pytest testi; testler gerçek veriye değil tests/ içindeki örneklere dayanır.
- .env, veri/ ve veritabanı dosyaları asla git'e girmez.
- Kod hesaplar, model konuşur: kalori, ortalama, hedef gibi sayılar her zaman koddan gelir.
- Koç tanı koymaz, ilaç önermez; sağlık yorumları kaynaklı olur (ileriki fazlar).
- Asıl çalışma ortamı Windows 11 + PowerShell. Saat dilimi Europe/Istanbul.

## Komutlar
- Çalıştır: uv run python -m koc bugun
- Haftalık: uv run python -m koc hafta
- Örnek veriyle: uv run python -m koc bugun --dosya tests/ornek_program.json
- Test: uv run pytest

## Yapı
koc/ kod · tests/ testler · veri/ kişisel veri (git dışı) · docs/ notlar ve rehberler
