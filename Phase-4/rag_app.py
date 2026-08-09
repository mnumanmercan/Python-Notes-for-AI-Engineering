import numpy as np
import voyageai
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
vo = voyageai.Client()
client = Anthropic()

# --- İNDEKSLEME (offline, bir kere) ---
documents = [
    "Şirketimizin iade politikası: ürünler 14 gün içinde iade edilebilir.",
    "Kargo süresi İstanbul içi 1 gün, diğer illere 2-3 gündür.",
    "Premium üyelik aylık 99 TL'dir ve ücretsiz kargo içerir.",
    "Müşteri hizmetlerine hafta içi 09:00-18:00 arası ulaşabilirsiniz.",
    "Genel müdürümüzün adı Ahmet Yılmaz'dır.",
]
doc_vecs = np.array(
    vo.embed(documents, model="voyage-4", input_type="document").embeddings
)

# --- SORGU (online, her soruda) ---
def rag_cevap(soru: str, k: int = 2) -> str:
    # 1) RETRIEVE — soruyu embed et, en benzer k chunk'ı bul
    q_vec = vo.embed([soru], model="voyage-4", input_type="query").embeddings[0]
    sims = np.dot(doc_vecs, q_vec)
    top_idx = np.argsort(sims)[::-1][:k]           # Faz 3 top-K refleksi
    context = "\n".join(documents[i] for i in top_idx)

    # 2) AUGMENT — context'i prompt'a göm
    prompt = f"""Aşağıdaki bağlamı kullanarak soruyu yanıtla.
Bağlamda cevap yoksa "Bu konuda bilgim yok" de, tahmin yürütme.

Bağlam:
{context}

Soru: {soru}"""
    print("PROMPT:\n", prompt)
    # 3) GENERATE — LLM context'e dayanarak cevap versin (Konu 1)
    response = client.messages.create(
        model="claude-sonnet-4-5", max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

print(rag_cevap("İade süresi kaç gün?"))
print(rag_cevap("Genel müdürün adı ne?"))   # context'te yok → "bilgim yok"