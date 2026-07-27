def logged(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} çağrıldı")
        result = func(*args, **kwargs)
        print("Sonuc: ", result)
        print(f"[LOG] {func.__name__} tamamlandı")
        return result
    return wrapper


@logged
def add(a,b):
    return a+b

result = add(3,5)
print(result)