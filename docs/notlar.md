# Notlar

## Sonraki fazlar için notlar

- **program.json şema doğrulaması:** Dosyanın yapısını pydantic veya SQLModel ile tanımlayıp her okumada kontrol et. Eksik veya hatalı alan erken yakalansın.
- **Gerçek kayıtlarla karşılaştırma:** Haftalık ortalama hedefi, ileride alınan gerçek kalori kayıtlarıyla karşılaştırılsın.
- **`bugun` için JSON çıktısı:** `--json` seçeneğiyle çıktı JSON olarak verilsin; web paneli ve iOS Kestirmeler bu veriyi okuyabilsin.
- **program.json yedeği:** Dosya git dışında olduğu için GitHub'da yedeği yok. Düzenli kopyası alınmalı.
- **7/24 çalışma:** Windows'ta servis veya zamanlanmış görev (Task Scheduler) ile sürekli çalıştırma seçenekleri değerlendirilsin.
- **Saat dilimi:** Tüm tarih hesapları `Europe/Istanbul` ile yapılsın; gece yarısı geçişlerinde (saat 00:00) gün değişimi kontrol edilsin.
- **tzdata güncelliği:** Saat dilimi veritabanı (tzdata) güncel tutulsun; yoksa saat hesapları yanlış çıkabilir.
- **Uzaktan erişim ve kimlik doğrulama:** Tailscale ile uzaktan erişim ve FastAPI fazında kimlik doğrulama (giriş kontrolü) planlansın.

## Faz 01 (bulut) notları

- GitHub deposu boştu; ana dal (`main`) `.gitignore` içeren ilk commit ile oluşturuldu.
- Kod ve belgeler alt ajanlarla (Sonnet ve Haiku) yazıldı; Opus denetledi.
