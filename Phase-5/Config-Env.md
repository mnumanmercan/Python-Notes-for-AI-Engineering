# Faz 5 · Konu 1 — Config & Secrets Yönetimi (pydantic-settings)

> **Tek cümlelik özet:** Ortam değişkenleri de "dışarıdan gelen güvenilmez girdidir" → onları `os.getenv` ile çıplak çekme, `pydantic-settings` ile **açılışta doğrula** (fail-fast, tipli, merkezi).

---

## 1. Neden `os.getenv` üretimde kırılgan?

| Problem | `os.getenv` / `os.environ` | Sonuç |
|---|---|---|
| **Tip** | Her zaman `str` döner (`"1024"`) | `max_tokens="1024"` → ya patlar ya *sessizce yanlış* çalışır |
| **Eksik değer** | `os.getenv` → `None` (hata yok) | Uygulama açılır, **saatler sonra** ilk çağrıda patlar (sebepten uzak hata) |
| **Doğrulama** | Yok | Config'e çöp yazılırsa üretimde fark edilir |

> 💡 **`os.environ[key]` vs `os.getenv(key)`**
> - `os.environ["KEY"]` → dict gibi, yoksa **anında `KeyError`** (fail-fast).
> - `os.getenv("KEY")` → yumuşak, yoksa **`None`** (geç patlar — daha tehlikeli).

**Prensip — "Parse, don't validate":** Güvenilmez girdiyi programın içine sokmadan önce tipli/doğrulanmış bir nesneye çevir. API body'sini titizlikle doğrulayıp config'i çıplak elle çekmek tutarsızlık.

---

## 2. Çözüm: `pydantic-settings`

`pydantic` (Faz 3) API body / LLM çıktısı doğrular. `pydantic-settings` **aynı motoru ortam değişkenleri + `.env` için** kullanır — yani Zod'un `envSchema.parse(process.env)` karşılığı.

```bash
uv add pydantic-settings
```

```python
# config.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # .env'i DOSYA konumuna sabitle (cwd'ye değil) — bkz. Bölüm 4
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env")

    anthropic_api_key: str          # zorunlu → yoksa AÇILIŞTA ValidationError
    voyage_api_key: str
    max_tokens: int = 1024          # ".env"de string "1024" → otomatik int coerce
    model: str = "claude-sonnet-4-5"
    request_timeout: float = 30.0
    log_level: str = "INFO"

settings = Settings()               # oku + doğrula + tiple
```

```python
# kullanım — os.getenv çağrıları koddan tamamen kalkar
from config import settings
client.messages.create(model=settings.model, max_tokens=settings.max_tokens, ...)
```

Kazanımlar: **tipli** (`max_tokens` gerçek `int`), **fail-fast** (eksik key açılışta patlar), **merkezi** (tek doğrulanmış nesne).

> 💡 `BaseSettings` = `BaseModel`'in env okuyan alt türü. Field adları case-insensitive eşleşir: `anthropic_api_key` ↔ `ANTHROPIC_API_KEY`.

---

## 3. `.env` dosyası doğru mu?

```dotenv
ANTHROPIC_API_KEY=sk-ant-...
VOYAGE_API_KEY=pa-...
MAX_TOKENS=1024
```

- Her satır **`KEY=value`** olmalı. `=` yoksa satır geçersiz → alan "missing" görünür.
- `.env` **mutlaka `.gitignore`'da** olmalı (secret'lar git'e girmez).
- Editör `.env.txt` diye kaydetmiş olabilir → dosya adını kontrol et.

---

## 4. ⚠️ Yaşanan 2 gerçek bug (can alıcı)

### Bug A — `env_file` cwd'ye görelidir, dosya konumuna değil
`env_file=".env"` → Python'un **çalıştırıldığın dizinde** (`pwd`) arar, `config.py`'nin yanında değil. Kökten çalıştırıp `.env` alt klasördeyse → bulamaz, **sessizce boş geçer**, tüm alanlar "missing".

Teşhis:
```bash
pwd
ls -la /path/to/.env    # dosya gerçekten burada mı, adı tam ".env" mi?
```

Kalıcı çözüm (cwd'den bağımsız):
```python
env_file=Path(__file__).parent / ".env"        # config.py ile aynı klasör
# .env bir üstteyse:
env_file=Path(__file__).parent.parent / ".env"
```
`../.env` çalışır ama hâlâ cwd'ye bağımlıdır — prod'da `Path(__file__)` desenini tercih et.

> **En sinsi taraf:** Dosya bulunamayınca pydantic **exception fırlatmaz**, boş geçer → hata "config yok" değil "alan eksik" gibi görünür, yanlış yöne bakarsın.

### Bug B — Coercion sihir değildir
- `MAX_TOKENS=1024` → `"1024"` → `int(1024)` ✅ (makul dönüşüm)
- `MAX_TOKENS=bin_yirmi_dört` → `int`'e çevrilemez → **açılışta ValidationError** ✅
- Ham girdi hata mesajında string görünür: `input_value={... 'max_tokens': '1024'}` → önce str alınır, doğrulama sırasında coerce edilir.

Coercion "makul dönüşüm yapar, uydurmaz" — config'e çöp yazarsan ilk saniyede yakalarsın.

---

## 5. İleri seviye bayrak — import yan etkisi

`settings = Settings()` modül seviyesinde → **import edildiği an çalışır**. Testte `from config import settings` dediğin an `.env` okunmaya zorlanır; CI'da `.env` yoksa test import'ta patlar.

Üretim deseni — doğrulamayı çağrıya ertele:
```python
from functools import lru_cache

@lru_cache                          # tek sefer hesapla, cache'le (Faz 2 decorator)
def get_settings() -> Settings:
    return Settings()
```
FastAPI'de `Depends(get_settings)` ile enjekte edilir → ileri konu.

---

## 6. Önemli Notlar

- Config = güvenilmez girdi → **sınırda doğrula**, açılışta patlat.
- `os.getenv` (str, sessiz None, geç patlama) ❌ → `pydantic-settings` (tipli, fail-fast) ✅
- `env_file` **cwd'ye görelidir** → `Path(__file__).parent` ile sabitle.
- Coercion makul dönüşüm yapar; çöpü açılışta yakalar.
- `.env` `.gitignore`'da; satırlar `KEY=value`.
- Modül seviyesi `Settings()` = import yan etkisi → prod'da `@lru_cache`'li `get_settings()`.