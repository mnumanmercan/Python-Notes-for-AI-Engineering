"""
Faz 5 · Konu 5 — Prompt Caching demosu

Senaryo: NovaBank müşteri destek asistanı. Uzun ve SABİT bir bilgi tabanı
(politikalar) her soruda tekrar gönderilir → cache'lemek için ideal.

Aynı sistem prompt'uyla 2 farklı soru soruyoruz:
  - 1. çağrı: cache YAZILIR (cache_creation_input_tokens dolu)
  - 2. çağrı: cache OKUNUR (cache_read_input_tokens dolu, ~0.1x fiyat)
"""


from anthropic import Anthropic, APIStatusError, APITimeoutError, RateLimitError
from config import settings
from pricing import hesapla_maliyet
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
# httpx gürültüsünü kıs (Konu 2 notu)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

client = Anthropic(
    api_key=settings.anthropic_api_key,
    timeout=settings.request_timeout,
    max_retries=2,
)

# --- SABİT bilgi tabanı: caching bunu bir kez işleyip saklayacak ---
# (Eşiği geçmesi için yeterince uzun; gerçekte belgelerin/RAG chunk'ların olurdu.)
BILGI_TABANI = """
NovaBank Müşteri Hizmetleri Bilgi Tabanı (Sürüm 2026.1)

1. HESAP TÜRLERİ
NovaBank üç bireysel hesap sunar: Standart, Artı ve Prestij. Standart hesap
ücretsizdir ve aylık işlem sınırı yoktur. Artı hesap aylık 49 TL'dir; yurt dışı
transferlerde indirim ve ayda 5 ücretsiz havale sağlar. Prestij hesap aylık
199 TL'dir; sınırsız ücretsiz havale, öncelikli müşteri hattı ve havaalanı
lounge erişimi içerir. Hesap yükseltmeleri anında geçerli olur; düşürmeler bir
sonraki fatura döneminde etkinleşir.

2. TRANSFER VE HAVALE
Yurt içi havaleler hafta içi 08:00-17:00 arası anında gerçekleşir; bu saatler
dışında bir sonraki iş gününde işlenir. EFT işlemleri saat başı gönderilir.
Yurt dışı transferler SWIFT ile 1-3 iş günü sürer. Günlük transfer limiti
Standart hesapta 50.000 TL, Artı hesapta 150.000 TL, Prestij hesapta
500.000 TL'dir. Limit artırımı için kimlik doğrulama ve gelir belgesi gerekir.

3. KART İŞLEMLERİ
Banka kartı başvurusu onaylandıktan sonra kart 3-5 iş gününde adrese ulaşır.
Kayıp/çalıntı kart bildirimi 7/24 destek hattından yapılır ve kart anında
bloke edilir. Kredi kartı asgari ödeme oranı dönem borcunun %20'sidir.
Temassız ödeme limiti işlem başına 1.500 TL'dir; üzerinde PIN istenir.

4. GÜVENLİK
NovaBank hiçbir zaman telefonda veya e-postada şifre, PIN veya SMS kodu
istemez. Şüpheli işlem tespit edilirse hesap geçici olarak dondurulur ve
müşteriye SMS ile bilgi verilir. İki adımlı doğrulama tüm hesaplarda
varsayılan olarak açıktır ve kapatılamaz.

5. KREDİLER
İhtiyaç kredisi başvuruları online yapılır ve genellikle 24 saat içinde
sonuçlanır. Faiz oranları kredi notuna göre değişir. Erken kapamada kalan
anaparanın %1'i kadar erken ödeme ücreti alınır (Prestij hesaplarda alınmaz).
Konut kredilerinde ekspertiz ücreti başvurana aittir.

6. İTİRAZ VE ŞİKAYET
İşlem itirazları 30 gün içinde yapılmalıdır. Şikayetler ortalama 5 iş gününde
yanıtlanır. Çözülemeyen şikayetler için Tüketici Hakem Heyeti'ne başvurulabilir.

7. MOBİL VE İNTERNET BANKACILIĞI
NovaBank mobil uygulaması iOS ve Android'de ücretsizdir. Uygulamaya ilk girişte
SMS ile doğrulama yapılır. Parmak izi ve yüz tanıma ile giriş desteklenir.
İnternet bankacılığı şifresi 90 günde bir değiştirilmelidir; 5 hatalı girişte
hesap 30 dakika kilitlenir. Mobil uygulamadan QR ile para çekme, fatura ödeme,
otomatik ödeme talimatı ve yatırım işlemleri yapılabilir. Uygulama üzerinden
günlük QR ile para çekme limiti 5.000 TL'dir.

8. YATIRIM ÜRÜNLERİ
NovaBank vadeli mevduat, döviz, altın ve yatırım fonu sunar. Vadeli mevduat
minimum tutarı 1.000 TL'dir ve vade sonundan önce bozulursa faiz işlemez.
Fon alım-satım emirleri iş günü 09:00-17:00 arası verilebilir; emirler ertesi
iş günü fiyatıyla gerçekleşir. Döviz ve altın alımında işlem ücreti alınmaz,
yalnızca alış-satış kuru farkı geçerlidir. Yatırım hesabı açmak için risk
profili anketi doldurulması zorunludur.

9. ÜCRET VE MASRAFLAR
Hesap işletim ücreti Standart hesapta yıllık 120 TL'dir; Artı ve Prestij
hesaplarda alınmaz. ATM'den nakit çekme kendi ATM'lerinde ücretsiz, başka banka
ATM'lerinde işlem başına 15 TL'dir. Hesap özeti dijital olarak ücretsizdir;
basılı özet talebi 25 TL'dir. Kapatılan hesaplarda kalan bakiye 3 iş günü
içinde belirtilen IBAN'a aktarılır.

10. MÜŞTERİ DESTEĞİ
Telefon desteği 7/24 açıktır. Canlı destek hafta içi 08:00-22:00 arası
çalışır. Prestij müşterileri öncelikli hatta yönlendirilir ve ortalama bekleme
süresi 30 saniyenin altındadır. Şube işlemleri için önceden randevu alınabilir.

Yanıt kuralı: Sadece bu bilgi tabanına dayan. Bilgi burada yoksa "Bu konuda
elimde bilgi yok, lütfen 0850 000 00 00 hattını arayın" de. Tahmin yürütme.
""".strip()


def sor(soru: str) -> None:
    """Bilgi tabanını cache'leyerek tek bir soru sorar, usage + maliyet loglar."""
    try:
        response = client.messages.create(
            model=settings.model,
            max_tokens=settings.max_tokens,
            system=[
                {
                    "type": "text",
                    "text": BILGI_TABANI,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": soru}],
        )
    except (RateLimitError, APITimeoutError, APIStatusError) as e:
        logger.error("API hatası | %s", type(e).__name__)
        return
    except Exception:
        logger.exception("Çağrı başarısız")
        raise

    u = response.usage
    logger.info(
        "usage | input=%s output=%s | cache_write=%s cache_read=%s",
        u.input_tokens, u.output_tokens,
        u.cache_creation_input_tokens, u.cache_read_input_tokens,
    )

    maliyet = hesapla_maliyet(
        settings.model,
        u.input_tokens,
        u.output_tokens,
        cache_write_tokens=u.cache_creation_input_tokens,   # doğru alan
        cache_read_tokens=u.cache_read_input_tokens,        # okuma da geçildi
    )
    logger.info("Maliyet | $%.6f", maliyet)

    print("SORU:", soru)
    print("CEVAP:", response.content[0].text, "\n")


if __name__ == "__main__":
    # Aynı sistem prompt'u (bilgi tabanı), farklı sorular
    logger.info("--- 1. çağrı (cache YAZILACAK) ---")
    sor("Prestij hesabın aylık ücreti ne kadar ve neler içeriyor?")

    logger.info("--- 2. çağrı (cache OKUNACAK) ---")
    sor("Yurt dışı transfer kaç iş günü sürer?")