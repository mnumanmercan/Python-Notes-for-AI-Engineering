import numpy as np
import voyageai
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
vo = voyageai.Client()
client = Anthropic()

documents = [
    "Python'da liste comprehension: [x*2 for x in range(5)] şeklinde yazılır.",
    "uv, pip'e göre çok daha hızlı bir Python paket yöneticisidir.",
    "FastAPI otomatik olarak /docs adresinde Swagger arayüzü sağlar.",
    "pydantic, gelen veriyi runtime'da doğrular ve tip zorlaması (coercion) yapar.",
    "Python'da async fonksiyonlar 'async def' ile tanımlanır.",
]

doc_vecs = vo.embed(documents, model="voyage-4", input_type="document").embeddings


def rag_answer(question: str, k: int = 2) -> str:
    query_vec=vo.embed([question], model="voyage-4", input_type="query").embeddings[0]
    sims = np.dot(doc_vecs, query_vec)
    top_answer = np.argsort(sims)[::-1][:k]
    context = "\n".join(documents[i] for i in top_answer)

    prompt = f"""
    Aşağıdaki bağlamı kullanarak soruyu yanıtla.
    Bağlamda cevap yoksa "Bu konuda bilgim yok" de, tahmin yürütme.

    Bağlam:
    <context>
        {context}
    </context>

    Soru: 
    <question>
        {question}
    </question>"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text

print(rag_answer("FastAPI dökümantasyonu nerede?"))
print(rag_answer("Django nasıl kurulur?"))