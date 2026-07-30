## Shallow vs Deep copy on JS and Python
- Shallow copy (sığ kopyalama) bir nesne ya da dizinin yalnızca en üst düzey (yüzeyindeki) özelliklerini kopyalar, iç içe durumda olan nesne ve dizilerde iç düzeydeki verilerin ise orijinal bellek referansını saklamaya devam eder. Yani kıyafet kopya ile değişir fakat içerik tamamen aynı kalı
- Deep Kopy ise tüm iç içe yapıdaki her şeyi yeni bağımsız bir alanına kopyalar.

    Neden önemli: AI tarafında config dict'leri, mesaj listeleri (messages=[{"role": ...}]) hep iç içe mutable yapılardır. Bir fonksiyona geçirip içini değiştirirsen çağıranın verisi de değişir — üretimdeki sinsi bug'ların klasiği.

---------------------
## Comprehension — Python'un map/filter'ı
![Comprehension](image.png)

----------------------
## *args (argumants) vs **kwargs (keyword & argumants)
![Kwargs](image-1.png)

----------------------
## Lambda - Arrow func benzer ama çok kısıtlı kullanım.
![Lambda](image-2.png)

----------------------
## Function Tanımlamaları ve argüman kullanımları
def.py herşeyi açıklıyor

----------------------
## Try-Catch
![Try-Catch](image-3.png)

    Sık göreceğin built-in hatalar: ValueError, KeyError, TypeError, IndexError, FileNotFoundError, ConnectionError.
    Not: except Exception: ile her şeyi yakalamak (JS'teki boş catch {} gibi) — gerçek bug'ları da yutar. Sadece beklediğin hataları yakala.
![Raise](image-4.png)

Else sadece hata olmazsa çalışır
![Else](image-5.png)

** Neden ÖNemlidir?
![AI API Calls Exceptions](image-6.png)

Exception kontrol ve koşulları?
![Pratik](image-7.png)

![Pratik 2](image-8.png)

----------------------
# Moduller ve Import Yapısı
JS ve Python import yapısı
![Import karşılıkları](image-9.png)

Pythonda export yoktur, her şey otomatik exporttur
![Export](image-11.png)