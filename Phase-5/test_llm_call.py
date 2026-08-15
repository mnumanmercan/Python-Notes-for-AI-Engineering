
from anthropic import Anthropic, APIStatusError, APITimeoutError, RateLimitError
from config import settings
from pricing import hesapla_maliyet
import logging

logging.basicConfig(
    level=logging.INFO,                                    # eşik: INFO ve üstü
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__) 


client = Anthropic(
    api_key=settings.anthropic_api_key,
    timeout=settings.request_timeout,
    max_retries=2,
)

example_paragraph = """
    When was the last time you were able to give 100% of your attention to a single task?

When you can give something your complete attention — which isn't always easy in a distraction-filled world — you'll do better quality work. You also get more done when you don't have to keep stopping for less important tasks!

So you might be interested in the idea of "deep work," which was named by American computer science professor and author Cal Newport.

In his book Deep Work: Rules for Focused Success in a Distracted World, Newport describes deep work as a state of deep concentration with no distractions, letting your brain function at its best.

But making time for deep work requires a plan and self-discipline — you can't just do it whenever you think of it.

So you should find time in your week when you can schedule deep work. And when you've done so, make sure other people know so they won't distract you during those blocks of time.

Be realistic too — you might not be ready or able to commit to, say, four straight hours of deep work! Try scheduling blocks of one hour to 90 minutes while you train your brain to get used to it. These can get longer as you develop your concentration skills.

No matter how long you plan to spend doing deep work, each session should have clear goals. The tasks that benefit most from deep work are things like writing reports and long documents, coding, or anything else that needs time and attention to detail, so prioritize these.

You need to find the right place for deep work too. This should be somewhere calm, quiet and as distraction-free as possible. If you can't find somewhere like this, try noise-canceling headphones to shut the world out!

With a bit of careful planning, it's not hard to make deep work a part of your regular work routine.
"""
try:
    logger.info("LLM çağrısı başlıyor | model=%s", settings.model)
    response = client.messages.create(
        model=settings.model,
        max_tokens=settings.max_tokens,
        system="Sen alanında uzman bir çevirmensin; sana verilen İngilizce cümleyi sadece Türkçeye çevir, daha sonra bu çeviri altına metnin özetini ekle. Başka bir şey yazma.",
        messages=[
            {"role": "user", "content": example_paragraph}
        ]
    )
    logger.info("Token usage | input=%s output=%s",
            response.usage.input_tokens, response.usage.output_tokens)

    maliyet = hesapla_maliyet(
        settings.model,
        response.usage.input_tokens,
        response.usage.output_tokens
    )

    logger.info("Maliyet | $%.6f", maliyet)
except RateLimitError:
    logger.error("Rate limit - SDK retry limit filled")
except APITimeoutError:
    logger.error("Timeout - API is very slow...")
except APIStatusError as e:
    logger.error("API error | status=%s", e.status_code)
except Exception as e:
    logger.exception("LLM çağrısı başarısız")
    raise
else:
    print(response.content[0].text)


