# Senaryo: Bir RAG sisteminde 5 belge chunk'ını query ile karşılaştırdın,
# her birinin similarity skoru ve metadata'sı var. Bunları bir DataFrame'de 
# toplayıp analiz edeceksin — gerçek retrieval sonrası yapılan iş.

import pandas as pd

data = {
    "chunk_id": [0, 1, 2, 3, 4],
    "source": ["doc_a.pdf", "doc_a.pdf", "doc_b.pdf", "doc_c.pdf", "doc_b.pdf"],
    "score": [0.91, 0.45, 0.88, 0.32, 0.76],
    "tokens": [120, 85, 200, 60, 150],
}

df = pd.DataFrame(data)
#print(df)

relevant = df[df["score"] > 0.7]
total_tokens = relevant["tokens"].sum()
ranked = df.sort_values("score", ascending=False)

print(df["score"] > 0.7)
print("0.7 den büyük skor: \n", relevant)
print("----------")
print("Toplam token:", total_tokens)
print("----------")
print("Rank: \n", ranked)