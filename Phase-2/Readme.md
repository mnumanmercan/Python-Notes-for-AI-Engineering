## 1-Type Hints
![TS <-> Python](image.png)

## 2-Değişken ve Koleksyon tipleri
    Tuple

![Değişken ve Koleksyon](image-1.png)

## 3-Dataclasses
![Dataclasses](image-2.png)

### 3.1-Birkaç kritik nokta:
![models.py](models.py)
- Alan sırası önemli — default'suz alanlar, default'lu alanlardan önce gelmeli (aynı fonksiyon parametrelerindeki gibi).
- Mutable default tuzağı yine burada — hatırla, fonksiyonlarda items=[] yasaktı. Dataclass'ta liste/dict default'u için field kullanılır:
    ![alt text](image-3.png)
### 3.2-Dataclass ile ilg 2 özellik:
1. Aynı dataclass üzerinden oluşturulan aynı içerikli obje karşılaştırması dataclass özelliği olarak kimlik değil değer karşılaştırması üzerinden değerlendirilir. 
    ![alt text](image-4.png)
2. Dict'e çevirme: Dataclass objesyi Bir API'ye JSON şeklinde göndermek istediğinde dict şeklinde göndermen gerekir. bu yüzden dict e çevirmen gerekir (asdict):
    ![Dataclass To Dict](image-5.png)

## 4-Decorators
Pratikte ne işine yarar?

En sık şu durumlarda görürsün: bir fonksiyonu çalıştırmadan önce/sonra ortak bir iş yapmak (loglama, süre ölçme, yetki kontrolü, önbellekleme) veya bir fonksiyonu bir sisteme kaydetmek (FastAPI'nin route'ları gibi). Ortak nokta şu: fonksiyonun kendi içeriğini kirletmeden ona dışarıdan davranış eklemek.
- Temel: Python'da fonksiyonlar da "obje"dir

    Bu, decorator'ların bel kemiği. Bir fonksiyonu değişkene atayabilir, başka fonksiyona argüman olarak geçebilir, bir fonksiyondan geri döndürebilirsin.
    ![Decorator](image-6.png)
    ![Decorator Tanım](image-7.png)
    ![Decorator Kısaltma](image-8.png)

## 5-Generators
    - Generator, "değerleri hepsini birden üretip bir listeye koymak yerine, teker teker, istendikçe üreten" özel bir fonksiyondur. İyi haber: JS'te bunun neredeyse birebir karşılığı var (function* ve yield)

![Yield](image-10.png)
* Nasıl kullanılır?
![Yield-2](image-11.png)
* Asıl faydası: bellek
![Yield-3](image-12.png)
* Genel örnek:
![Token Streaming](image-14.png)


    - List Comprehesion: Python gibi programlama dillerinde mevcut bir listeden veya döngüden kısa, hızlı ve okunabilir yeni bir liste üretme yöntemidir
        ![List-comp](image-13.png)

## 6-async/await
![async-await](image-15.png)

Async yapısının JS ten farkları:
    -   asyncio.run -> JS'te <func_call> yazdığın an fonksiyon hemen çalışmaya başlar ve sana çalışan bir Promise döner. Python'da ise coroutine tembeldir: onu ya await etmen ya da bir event loop'a vermen gerekir, yoksa ölü durur.
        ![alt text](image-16.png)
    -   işleri Eşzamanlı yürütmek için: gather
        ![gather](image-17.png)