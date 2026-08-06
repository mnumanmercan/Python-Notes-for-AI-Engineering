import pandas as pd

# Series = tek sütun (isimli numpy array gibi)
# DataFrame = tüm tablo (satırlar + sütunlar)

df = pd.DataFrame({
    "name": ["Numan", "Linus", "Guido"],
    "followers": [42, 315000, 78000],
    "language": ["JS", "C", "Python"],
})

print(df)
print(df["followers"])          # tek sütun (Series)
print(df["followers"].mean())   # ortalama — vektörel, döngüsüz