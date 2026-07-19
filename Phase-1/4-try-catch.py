def safe_divide(a, b):
    try:
        #Bunun incelikli bir yanı da var: try bloğunu olabildiğince küçük tutmak iyi pratiktir — sadece patlayabilecek satır (a / b) içeride olmalı ki neyi yakaladığın belli olsun.
        result = a / b
        print(f"Sonuç: {result}")
        return result
    except ZeroDivisionError as e:
        print(f"Sıfıra bölünemez: {e}")
        None #return none olmadan da yapılabilir fakat kod okunurluğunda return none daha bilinçli bir girdiyi temsil eder.
    except TypeError as e:
        print(f"Sayı tipine uygun girmelisin: {e}")
        return None

safe_divide(10, 2)
safe_divide(5, 0)
safe_divide("abc", 2)

