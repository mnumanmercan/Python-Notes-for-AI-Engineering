## httpx
-   httpx, Python'ın modern HTTP istemcisidir — JS'teki fetch veya axios gibi. Yani bir sunucuya HTTP isteği (GET, POST vb.) atıp cevabı almak için kullanılır.
-   httpx'in requests (pythonda http istekleri için kullanılan benzer yapı)'ten ayrıldığı asıl nokta: httpx hem senkron hem de async çalışabilir.
    - LLM sdk ler perde arkasında bunu kullanır.
```python
import httpx
# client'ı aç
async with httpx.AsyncClient() as client:
    # istek at, await et
    response = await client.get(url)
    # hata varsa exception fırlat
    response.raise_for_status()
    # JSON gövdesini dict'e çevir
    data = response.json()

```
![httpx](image.png)
### Neden AsyncClient
    ![AsyncClient](image-1.png)

    Örnek kod: 
    ![ornek-kod](/Phase-3/1-httpx.py)
    ![note](image-2.png)

### with
    ![with](image-4.png)