## 1 - Anthropic SDK
![Anthropic-sdk](/Phase-4/anthropic_app.py)
![Output](image.png)

### İlk llm çağrısı
```python
    import os
    from dotenv import load_dotenv
    from anthropic import Anthropic

    load_dotenv()
    api_key = os.environ["ANTHROPIC_API_KEY"]

    client = Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="Sen alanında uzman bir çevirmensin; sana verilen İngilizce cümleyi sadece Türkçeye çevir, başka hiçbir şey yazma",
        messages=[
            {"role": "user", "content": "The cat is sleeping on the warm keyboard."}
        ]
    )

    print(response.content[0].text)
```
![Output-llm](image-2.png)
### Bound nedir?
![Bound-types](image-3.png)
### Async çağrı ve Sync çağrı:
![Llm-call-types](image-4.png)
Async örneği ![Async_call](/Phase-4/llm_multiple_call.py)

## 2 - Structured Output
![Structured_output](image-5.png)
```python
    from pydantic import BaseModel
    from anthropic import Anthropic

    class ContactInfo(BaseModel):
        name: str
        email: str
        plan_interest: str
        demo_requested: bool

    client = Anthropic()

    response = client.messages.parse(          # create değil → parse
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Şu e-postadan bilgi çıkar: John Smith (john@acme.com) "
                    "Enterprise planıyla ilgileniyor ve salı 14:00'e demo istiyor.",
        }],
        output_format=ContactInfo,             # pydantic modelini DAYAT
    )

    print(response.parsed_output)              # → doğrulanmış ContactInfo objesi
    print(response.parsed_output.email)        # nokta erişimi, garantili tip 
```

### Ürün yorumundan structured output
![product_comments](image-6.png)

### Literal
-   Typescript'te ki union'ların benzeri, fakat kullanım pipe operatoru "|" ile değil Literal ile tanımlanabilir

## 3 - Tool Use/Function calling
    LLM tek başına şunları yapamaz: güncel veriye erişmek (hava, stok, DB'deki sipariş), güvenilir matematik, dış dünyada bir eylem (e-posta gönder, kayıt oluştur). Tool use = modele "şu fonksiyonları çağırabilirsin" demek. Model hangi fonksiyonu ne zaman, hangi argümanlarla çağıracağına kendi karar verir.
![Tool-use-loop](image-7.png)