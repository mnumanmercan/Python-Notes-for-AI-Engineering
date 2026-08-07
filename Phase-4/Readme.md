## Anthropic SDK
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