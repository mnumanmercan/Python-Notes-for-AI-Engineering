# Faz 4 — Konu 3: Tool Use / Function Calling

> Anthropic SDK ile LLM'e "eller" verme. Agent'ların kalbi.
> Faz 4 ilerleme: 3/6 ✅

---

## 1. Neden Tool? (Temel Motivasyon)

LLM tek başına şunları **yapamaz**:

- Güncel / canlı veriye erişmek (hava durumu, stok, DB'deki sipariş, döviz kuru)
- Güvenilir matematik / hesaplama
- Dış dünyada bir **eylem** (e-posta gönder, kayıt oluştur, ödeme başlat)

**Tool use** = modele "şu fonksiyonları çağırabilirsin" demek. Model, **hangi** fonksiyonu, **ne zaman**, **hangi argümanlarla** çağıracağına kendisi karar verir.

> Zihinsel model: **model = beyin, sen = eller.**
> Model "şunu yap" der → sen yaparsın → sonucu geri verirsin → model konuşur.

---

## 2. Key Tanımlar (Sözlük)

| Terim | Ne demek |
|-------|----------|
| **tool** | Modele tanıttığın, çağırabileceği bir fonksiyon. |
| **tool tanımı** | Fonksiyonun modele "tarifi": `name` + `description` + `input_schema`. Model senin Python kodunu görmez, sadece bu tarifi görür. |
| **`input_schema`** | Fonksiyonun beklediği argümanları anlatan JSON Schema. Modelin doğru argüman üretmesini sağlar. |
| **`tool_use` bloğu** | Modelin cevabındaki "şu tool'u şu argümanlarla çağırmak istiyorum" mesajı. İçinde `name`, `input`, `id` var. |
| **`tool_result` bloğu** | Senin fonksiyonu çalıştırıp sonucu modele geri verdiğin mesaj. `tool_use_id` ile ilgili çağrıya bağlanır. |
| **`stop_reason`** | Modelin neden durduğu: `"tool_use"` = tool çağırmak için durdu; `"end_turn"` = düz cevap verip bitirdi. |
| **inversion of control** | Fonksiyonunu ne zaman çağıracağına *model* karar verir, sen değil. (FastAPI'de bu kararı uvicorn veriyordu.) |

---

## 3. En Kritik Kavram

> **Model senin fonksiyonunu ÇALIŞTIRMAZ.**
> Sadece "şu tool'u şu argümanlarla çağırmak istiyorum" der (`tool_use`).
> Fonksiyonu **sen** çalıştırıp sonucunu geri verirsin (`tool_result`).

Bu, Faz 3'teki FastAPI **inversion-of-control**'ün ikizi:
- FastAPI: *uvicorn* senin route fonksiyonunu ne zaman çağıracağına karar verirdi.
- Tool use: *model* senin fonksiyonunu ne zaman çağıracağına karar verir.

---

## 4. Döngü (5 Adım)

1. Tool'ları tanımla, `create(...)`'a `tools=` ver.
2. Model karar verir → cevap `stop_reason: "tool_use"`, içinde `tool_use` bloğu (`name`, `input`, `id`).
3. **Sen** o argümanlarla gerçek fonksiyonu çalıştırırsın.
4. Sonucu `tool_result` bloğu olarak geri gönderirsin (aynı `id` ile eşleşir).
5. Model sonucu okuyup **nihai metin** cevabını üretir.

```
[user soru] → [assistant tool_use] → [user tool_result] → [assistant nihai cevap]
```

---

## 5. Tam Örnek (yorumlu)

```python
# 1) Gerçek fonksiyon — asıl işi yapan (gerçekte DB sorgusu olurdu)
def siparis_durumu(siparis_no: str) -> str:
    veritabani = {
        "1001": "Kargoya verildi, tahmini teslim yarın.",
        "1002": "Hazırlanıyor.",
        "1003": "Teslim edildi.",
    }
    return veritabani.get(siparis_no, "Sipariş bulunamadı.")

# 2) Tool tanımı — modele fonksiyonu TARİF eder (model Python kodunu görmez)
tools = [{
    "name": "siparis_durumu",           # modelin çağıracağı isim
    "description": "Sipariş numarasına göre siparişin durumunu getirir.",  # NE ZAMAN çağıracağını buna göre karar verir
    "input_schema": {                   # hangi argümanları beklediği
        "type": "object",
        "properties": {
            "siparis_no": {"type": "string", "description": "Sorgulanan sipariş numarası"}
        },
        "required": ["siparis_no"],
    },
}]

messages = [{"role": "user", "content": "1002 numaralı siparişim ne durumda?"}]

# 3) İlk çağrı — model tool istemeye karar verir
response = client.messages.create(
    model="claude-sonnet-4-5", max_tokens=1024,
    tools=tools, messages=messages,
)
print(response.stop_reason)   # "tool_use"

# 4) tool_use bloğunu bul (content bir LİSTE → tipe göre filtrele)
tool_use = next(b for b in response.content if b.type == "tool_use")
# tool_use.name  → "siparis_durumu"
# tool_use.input → {"siparis_no": "1002"}
# tool_use.id    → eşleştirme kimliği

# 5) Fonksiyonu SEN çalıştır (** ile dict'i argümanlara aç)
result = siparis_durumu(**tool_use.input)

# 6) Sonucu geri gönder — konuşmayı büyüterek
messages.append({"role": "assistant", "content": response.content})   # modelin tool_use mesajı
messages.append({"role": "user", "content": [{
    "type": "tool_result",
    "tool_use_id": tool_use.id,   # hangi çağrının sonucu
    "content": result,
}]})

# 7) İkinci çağrı — model sonucu okuyup nihai cevabı yazar
final = client.messages.create(
    model="claude-sonnet-4-5", max_tokens=1024,
    tools=tools, messages=messages,
)
print(final.content[0].text)   # "1002 numaralı siparişiniz hazırlanıyor..."
```

---

## 6. Satır Satır Anlam (Takılınan Noktalar)

**`next(b for b in response.content if b.type == "tool_use")`**
`response.content` bir **listedir**; içinde metin bloğu da, tool_use bloğu da olabilir. Bu satır listeyi gezip `type == "tool_use"` olan **ilk** bloğu bulur. `content[0]` yazılmaz çünkü ilk blok bazen metin olabilir → tipe göre bulmak güvenli. (`next(...)` + generator expression = "koşulu sağlayan ilkini al".)

**`result = siparis_durumu(**tool_use.input)`**
`tool_use.input` bir dict: `{"siparis_no": "1002"}`. `**` bunu açar → `siparis_durumu(siparis_no="1002")`. Modelin istediği argümanlarla senin gerçek fonksiyonunu çalıştırıyorsun.

**İki `append` satırı**
`messages` listesine iki mesaj eklenir: modelin `tool_use`'u (assistant) + senin `tool_result`'ın (user). Böylece geçmiş `[user] → [assistant tool_use] → [user tool_result]` şeklinde tamamlanır. Model stateless olduğu için 2. çağrıda bu geçmişin tamamını tekrar görmesi gerekir.

**2. çağrıda `content[0].text` yeterli**
O turda model tool çağırmayıp düz metin döndürdüğü için ilk blok direkt metindir.

---

## 7. 💡 Önemli İç Görüler

- **`content` neden liste?** (Konu 1'in cevabı) İçinde `text` de `tool_use` de olabilir. O yüzden `content[0]` yerine `b.type`'a göre filtreleriz.

- **`tool_result` neden `tool_use_id` ister?** Model tek turda birden fazla tool çağırabilir; sonuçları doğru çağrıyla eşleştirmek için her `tool_use`'un bir `id`'si vardır, `tool_result` onu referans verir (↔ request/response eşleştirme id'si).

- **Konuşmayı neden büyütüyoruz?** LLM **stateless**'tir — her çağrı bağımsız. Modelin "tool istemiştim, işte cevabı" bağlamını görmesi için `tool_use` + `tool_result`'ı `messages`'a ekleyip geçmişi geri gönderiyoruz. Bu büyüyen liste = **hafıza** → Konu 6'daki agent hafızasının çekirdeği.

- **`description` bir dokümantasyon değil, TALİMATtır.** Onu insana değil, modele yazıyorsun: "bu tool ne işe yarar, ne zaman kullanılır". Kötü `description` = yanlış zamanda / hiç çağrılmayan tool.

- **`tools=tools` her çağrıda tekrar verilir.** Stateless olduğu için model tool'ları "hatırlamaz"; ayrıca konuşmada `tool_use`/`tool_result` varken `tools` parametresi zorunludur.

- **`tool_result`'ı geri göndermezsen** model nihai cevabı **üretemez** — ilk turda sadece "tool çağırmak istiyorum" demişti, sonucu görmedi.

---

## 8. İleri Notlar (Üretim / Sonraki Adımlar)

- **pydantic bağlantısı:** `input_schema`'yı elle yazmak yerine bir pydantic modelinden `MyModel.model_json_schema()` ile üretebilirsin.
- **`strict: True`:** Konu 2'deki constrained decoding tool argümanlarına da uygulanır → argümanların şemaya birebir uyması garanti.
- **Çoklu / paralel tool:** Model tek turda birden fazla `tool_use` bloğu dönebilir. Bunları Faz 3'teki `asyncio.gather` refleksiyle **paralel** çalıştırabilirsin.
- **Agent döngüsü (Konu 6):** Bu 5 adımlık döngüyü bir `while` içine alıp `stop_reason == "tool_use"` olduğu sürece döndürmek = temel agent.

---

## 9. Tek Cümlelik Özet

> **Model beyin, sen ellersin.** Model "şunu yap" der (`tool_use`) → sen yaparsın (fonksiyon) → sonucu geri verirsin (`tool_result`) → model konuşur. Konuşma listesi bu gidiş-gelişte büyüyerek hafıza görevi görür.
