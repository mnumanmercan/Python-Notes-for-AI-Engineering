import os
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
from typing import Literal

load_dotenv()
api_key = os.environ["ANTHROPIC_API_KEY"]

client = Anthropic()
# 1) Gerçek fonksiyon (şimdilik mock)
def siparis_durumu(siparis_no: str) -> str:
    veritabani = {
        "1001": "Kargoya verildi, tahmini teslim yarın.",
        "1002": "Hazırlanıyor.",
        "1003": "Teslim edildi.",
    }
    return veritabani.get(siparis_no, "Sipariş bulunamadı.")

# 2) Tool tanımı — modele fonksiyonu TARİF eder
tools = [{
    "name": "siparis_durumu",
    "description": "Kullanıcının sipariş durum sorgulaması için ona sipariş durumunu gösteren bir structured output ver.",
    "input_schema": {
        "type": "object",
        "properties": {"siparis_no": {"type": "string", "description": "Sorgulanan sipariş numarası"}},
        "required": ["siparis_no"],
    },
}]

messages = [{"role": "user", "content": "1004 No'lu siparişin durumu nedir?"}]

# 3) İlk çağrı — model tool istemeye karar verir
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages,
)

print(response.stop_reason)   # "tool_use"

# 4) tool_use bloğunu bul (content bir LİSTE — işte şimdi anlam kazandı)
tool_use = next(b for b in response.content if b.type == "tool_use")
print(tool_use)
print(tool_use.input)

# 5) Fonksiyonu SEN çalıştır
result = siparis_durumu(**tool_use.input)   # ** unpacking (Faz 3 refleksi)

# 6) Sonucu geri gönder — konuşmayı büyüterek
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": [{
    "type": "tool_result",
    "tool_use_id": tool_use.id,     # id ile eşleşir
    "content": result,
}]})

# 7) İkinci çağrı — model sonucu okuyup nihai cevabı yazar
final = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools, 
    messages=messages,
)
print(final.content[0].text)