import os
from dotenv import load_dotenv
import asyncio
from anthropic import AsyncAnthropic   # Anthropic → AsyncAnthropic
load_dotenv()
api_key = os.environ["ANTHROPIC_API_KEY"]

client = AsyncAnthropic()

async def cevir(cumle: str) -> str:
    response = await client.messages.create(   # await eklendi
        model="claude-sonnet-4-5",
        max_tokens=512,
        system="Sana verilen İngilizce cümleyi sadece Türkçeye çevir.",
        messages=[{"role": "user", "content": cumle}],
    )
    return response.content[0].text

async def main():
    cumleler = [
        "The cat is sleeping.",
        "It rains in Istanbul.",
        "Python is fun.",
    ]
    sonuclar = await asyncio.gather(*(cevir(c) for c in cumleler))
    for c, s in zip(cumleler, sonuclar):
        print(f"{c} → {s}")

asyncio.run(main())