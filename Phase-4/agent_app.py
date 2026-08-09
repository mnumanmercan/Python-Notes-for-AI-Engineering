import numpy as np
import voyageai
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
vo = voyageai.Client()
client = Anthropic()

# --- Gerçek fonksiyonlar (mock) ---
def urun_fiyati(urun: str) -> int:
    return {"Airpods": 5000, "iPhone": 60000}.get(urun, 0)

def kdv_hesapla(fiyat: int) -> int:
    return int(fiyat * 1.20)   # %20 KDV


# --- Dispatcher: tool adı → gerçek fonksiyon ---
TOOL_FONKSIYONLARI = {
    "urun_fiyati": urun_fiyati,
    "kdv_hesapla": kdv_hesapla,
}

# --- Tool tanımları ---
tools = [
    {
        "name": "urun_fiyati",
        "description": "Bir ürünün KDV hariç fiyatını TL olarak getirir.",
        "input_schema": {
            "type": "object",
            "properties": {"urun": {"type": "string"}},
            "required": ["urun"],
        },
    },
    {
        "name": "kdv_hesapla",
        "description": "Verilen fiyata %20 KDV ekleyip toplam fiyatı döndürür.",
        "input_schema": {
            "type": "object",
            "properties": {"fiyat": {"type": "integer"}},
            "required": ["fiyat"],
        },
    },
]

# --- AGENT DÖNGÜSÜ ---
def agent(soru: str) -> str:
    messages = [{"role": "user", "content": soru}]
    step_count: int = 0

    while True:                                    # ← döngü = otonomi
        response = client.messages.create(
            model="claude-sonnet-4-5", max_tokens=1024,
            tools=tools, messages=messages,
        )

        if response.stop_reason != "tool_use":     # ← çıkış: model tatmin oldu
            return response.content[0].text

        if step_count == 5:
            break
        # Modelin tool isteğini hafızaya ekle
        messages.append({"role": "assistant", "content": response.content})

        # Tüm tool_use bloklarını çalıştır (aynı turda birden fazla olabilir)
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  🔧 {block.name}: {block.input}")   # adımları görmek için
                sonuc = TOOL_FONKSIYONLARI[block.name](**block.input)  # dispatcher
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(sonuc),          # tool_result içeriği string olmalı
                })

        messages.append({"role": "user", "content": tool_results})

print(agent("Airpods'un KDV dahil fiyatı ne kadar?")) ## 2 tool (fiyat + kdv toolu) çağırır
print(agent("iPhone kaç para, KDV hariç?")) ## 1 tool (fiyat) çağırır