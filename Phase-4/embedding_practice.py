import voyageai
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
api_key = os.environ["VOYAGE_API_KEY"]

vo = voyageai.Client()

documents = [
    "Python programlama dili veri bilimi için çok popülerdir.",
    "Kediler günde ortalama 15 saat uyur.",
    "FastAPI, async destekli modern bir Python web framework'üdür.",
    "Kahve çekirdekleri kavrulduktan sonra öğütülür.",
]

doc_vecs = vo.embed(documents, model="voyage-4", input_type="document").embeddings

print("------------")

query = "async web geliştirme aracı"
query_vec = vo.embed([query], model="voyage-4", input_type="query").embeddings[0]


similarities = np.dot(doc_vecs, query_vec)
best = np.argsort(similarities)[::-1][:2]
for i in best:
    print(f"{similarities[i]:.3f} → {documents[i]}")

