import voyageai
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
api_key = os.environ["VOYAGE_API_KEY"]

vo = voyageai.Client()

import numpy as np

documents = [
    "Akdeniz diyeti balık, zeytinyağı ve sebzeye dayanır.",
    "Fotosentez ışık enerjisini glikoza çevirir ve oksijen üretir.",
    "Apple'ın çeyrek sonuç toplantısı 2 Kasım Perşembe saat 14:00'te.",
    "Nehirler su, sulama ve canlılara yaşam alanı sağlar.",
]

# 1) Belgeleri embed et
doc_vecs = vo.embed(documents, model="voyage-4", input_type="document").embeddings

# 2) Sorguyu embed et
query = "Apple'ın telekonferansı ne zaman?"
query_vec = vo.embed([query], model="voyage-4", input_type="query").embeddings[0]

# 3) Benzerlik: dot product
similarities = np.dot(doc_vecs, query_vec)   # her belge ile sorgunun benzerliği

# 4) En benzeri getir (Faz 3: np.argmax)
best = np.argmax(similarities)
print(documents[best])   # → Apple toplantısı cümlesi