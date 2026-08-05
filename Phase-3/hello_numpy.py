import numpy as np

## Bolum 1 
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    numerator = a @ b
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    return float(numerator / denominator)

v1 = np.array([1.0, 0.0, 1.0])
v2 = np.array([1.0, 0.0, 0.9])   # v1'e çok yakın
v3 = np.array([0.0, 1.0, 0.0])   # v1'e dik (ilgisiz)

print(cosine_similarity(v1, v2))  # ~1'e yakın olmalı
print(cosine_similarity(v1, v3))  # ~0 olmalı

## Bolum 2 
query = np.array([1.0, 0.2, 0.1])
docs = [
    np.array([0.9, 0.1, 0.0]),   # doc 0
    np.array([0.1, 0.9, 0.2]),   # doc 1
    np.array([1.0, 0.3, 0.1]),   # doc 2
]

scores = [cosine_similarity(query, doc) for doc in docs]

best = np.argmax(scores)

print("Skorlar:", scores)
print("En benzer doc:", best, "skor:", scores[best])