# Laptop kurulumu (Windows 11)

Bu belge, Koç projesini Windows 11 laptopunda sıfırdan kurup çalıştırmak için adım adım rehberdir. Tüm komutlar **PowerShell** içinde yazılır.

> **PowerShell nasıl açılır?** Başlat menüsüne `PowerShell` yaz ve **Windows PowerShell**'i aç. Bu belgedeki her kod bloğunu kopyalayıp PowerShell penceresine yapıştırıp Enter'a bas.

Bazı terimler:

- **Git:** Kod deposunu (projenin tüm dosyalarının ve geçmişinin tutulduğu yer) bilgisayara indirmeye yarayan programdır.
- **Depo (repository):** Projenin dosyalarının ve değişiklik geçmişinin bulunduğu klasördür.
- **GitHub:** Depoların internette saklandığı sitedir.
- **uv:** Python'u ve projenin ihtiyaç duyduğu kütüphaneleri kuran küçük bir araçtır.
- **Terminal:** Komutları yazıp çalıştırdığın siyah/mavi pencere (burada PowerShell).

---

## Adım 1: Git ve Claude Code kurulumu

### 1a. Git for Windows kur

Git'i şu komutla kur:

```powershell
winget install --id Git.Git -e
```

Bu komut, Windows'un kendi paket yöneticisi olan `winget` ile Git'i indirip kurar.

### 1b. Claude Code kur

Claude Code, terminalden çalışan yapay zekâ asistanıdır. Şu komutla kur:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Bu komut, Claude Code kurulum dosyasını internetten alıp hemen çalıştırır.

### 1c. Kurulumu kontrol et

Kurulumun çalıştığını görmek için:

```powershell
claude --version
```

Bu komut kurulu Claude Code sürümünün numarasını yazdırır.

> **Önemli:** Git veya Claude Code kurulduktan sonra PowerShell penceresini **kapatıp yeniden aç**. Yeni kurulan programların komutları ancak yeni pencerede tanınır.

---

## Adım 2: uv kurulumu

uv, Python'u ve proje kütüphanelerini kuracak araçtır. Kur:

```powershell
winget install --id=astral-sh.uv -e
```

Kontrol et:

```powershell
uv --version
```

Sürüm numarası çıkarsa kurulum tamam. Çıkmazsa PowerShell'i kapatıp yeniden aç.

---

## Adım 3: Depoyu bilgisayara indirme (klonlama)

"Klonlama" (clone), GitHub'daki depoyu kendi bilgisayarına kopyalamak demektir.

Önce proje için bir klasör oluştur:

```powershell
mkdir C:\Projeler
```

Bu komut `C:\Projeler` adında boş bir klasör oluşturur.

Bu klasöre geç:

```powershell
cd C:\Projeler
```

`cd` komutu, PowerShell'in çalıştığı klasörü değiştirir.

Depoyu indir:

```powershell
git clone https://github.com/Ataumutycl/Koc- koc
```

Bu komut depoyu GitHub'dan alır ve `koc` adında bir klasöre koyar.

Proje klasörüne gir:

```powershell
cd koc
```

**Neden `C:\Projeler` ve `koc`?**

- Yolda **Türkçe karakter** (ç, ğ, ı, ö, ş, ü) ve **boşluk** olmamalı. Bunlar bazı Python araçlarında hataya yol açabilir.
- Proje **OneDrive dışında** olmalı. OneDrive, dosyaları buluta eşitleyen Microsoft servisidir. Eşitleme, `.venv` klasörünü (proje için kurulan Python ortamını) bozabilir. Bu yüzden `Masaüstü` veya `Belgeler` gibi OneDrive'a bağlı klasörlere klonlama.

---

## Adım 4: `veri` klasörü ve program dosyası

Projenin kişisel verileri (`program.json`, antrenman ve beslenme programın) `veri` klasöründe tutulur.

Klasörü oluştur:

```powershell
mkdir veri
```

Şimdi **kendi `program.json` dosyanı** bu klasöre koy. Dosyanın tam yolu şöyle olmalı:

```
C:\Projeler\koc\veri\program.json
```

Kolay yol: Dosya Gezgini'nde `program.json` dosyasını bul, kopyala (Ctrl+C) ve `C:\Projeler\koc\veri` klasörünün içine yapıştır (Ctrl+V).

> **Neden GitHub'a gitmiyor?** `veri` klasörü, projedeki `.gitignore` dosyasına yazılmıştır. `.gitignore`, Git'e "bu klasörü/dosyayı takip etme" talimatı veren bir listedir. Böylece kişisel verilerin internete yüklenmez. Bu aynı zamanda şu anlama gelir: `veri` klasörünü Git ile yedekleyemezsin; yedeğini kendin almalısın.

---

## Adım 5: Python'u ve kütüphaneleri kur, programı çalıştır

### 5a. Proje ortamını kur

```powershell
uv sync
```

Bu komut Python 3.12'yi ve projenin ihtiyaç duyduğu tüm kütüphaneleri otomatik kurar. İlk seferde birkaç dakika sürebilir.

### 5b. Testleri çalıştır

```powershell
uv run pytest
```

Bu komut projenin otomatik testlerini çalıştırır. Sonunda **`passed`** kelimesini görmelisin (örneğin `15 passed` gibi; sayı test sayısına göre değişir). `failed` veya `error` görürsen bu kurulumda bir sorun var demektir; Claude'a veya bana haber ver.

### 5c. Günlük özeti gör

```powershell
uv run python -m koc bugun
```

Bu komut bugünkü antrenman ve beslenme hedefini gösterir. Beklenen çıktı örneği:

```
Bugün Pazartesi — antrenman günü: 1980 kcal, 170 g protein
```

### 5d. Haftalık özeti gör

```powershell
uv run python -m koc hafta
```

Bu komut haftanın tamamının özetini gösterir.

> **Not:** `uv run` komutu, projenin kendi Python ortamında çalıştırır. Bu yüzden `python` yerine her zaman `uv run python` yazıyoruz.

---

## Adım 6: Claude Code ile çalışmaya başla

Proje klasörüne geç ve Claude'u başlat:

```powershell
cd C:\Projeler\koc
claude
```

Bu komut, Claude Code'u proje klasöründe yeni bir oturumda açar.

Claude, açılışta projenin kökündeki `CLAUDE.md` dosyasını otomatik okur. Bu dosya, Claude'a projenin kuralları ve nasıl çalışacağı hakkında bilgi verir. Bu sayede her oturumda baştan anlatmana gerek kalmaz.

---

## Sık karşılaşılan sorunlar

| Belirti | Ne yapmalı |
|---|---|
| `winget`, `git`, `uv` veya `claude` komutu tanınmıyor | PowerShell'i kapatıp yeniden aç. Hâlâ olmuyorsa kurulumu tekrar çalıştır. |
| Türkçe karakterler (ş, ğ, ı) bozuk görünüyor | **Windows Terminal** uygulamasını kullan (Microsoft Store'dan kurulur). Ya da PowerShell'de önce `chcp 65001` yaz ve Enter'a bas. |
| "Program dosyası bulunamadı" hatası | `C:\Projeler\koc\veri\program.json` dosyasının orada olduğunu kontrol et. Dosya adı tam olarak `program.json` olmalı. |
| Proje güncellendi, yeni değişiklikleri almak istiyorum | Proje klasöründe `git pull` yaz. Bu, GitHub'daki en son sürümü bilgisayarına indirir. |

---

## Özet kontrol listesi

1. Git ve Claude Code kuruldu, `claude --version` çalıştı.
2. uv kuruldu, `uv --version` çalıştı.
3. Proje `C:\Projeler\koc` içine klonlandı.
4. `program.json` dosyası `C:\Projeler\koc\veri\` içinde.
5. `uv sync` bitti, `uv run pytest` sonunda `passed` gösterdi, `bugun` ve `hafta` komutları çalıştı.
6. `claude` komutu proje klasöründe açıldı.
