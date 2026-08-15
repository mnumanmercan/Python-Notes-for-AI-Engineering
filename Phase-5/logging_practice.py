from config import settings
import logging

logging.basicConfig(
    level=logging.INFO,                                    # eşik: INFO ve üstü
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)   # modül adıyla logger al (__name__ = dosya adı)

logger.debug("ham embedding vektörü: ...")   # INFO eşiğinin altında → BASILMAZ
logger.info("5 chunk getirildi")             # basılır
logger.warning("voyage API yavaş, 2s sürdü") # basılır
logger.error("LLM çağrısı başarısız") 