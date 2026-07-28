import asyncio

async def veri_cek(isim, saniye):
    print(f"{isim}: başladı")
    await asyncio.sleep(saniye)      # bir ağ isteğini taklit ediyor
    print(f"{isim}: bitti ({saniye}sn)")
    return f"{isim} sonucu"

async def main():
    sonuclar = await asyncio.gather(
        veri_cek("A", 2),
        veri_cek("B", 1),
        veri_cek("C", 3),
    )
    print(sonuclar)

asyncio.run(main())