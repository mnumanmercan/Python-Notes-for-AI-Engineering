import asyncio


async def fetch_user_simple(user_id):
    await asyncio.sleep(1)
    return f"user_{user_id}"

async def fetch_user_order(isim, saniye):
    print(f"{isim}: başladı")
    await asyncio.sleep(saniye)      # bir ağ isteğini taklit ediyor
    print(f"{isim}: bitti ({saniye}sn)")
    return f"{isim} sonucu"

async def main():
    result = await asyncio.gather(
        fetch_user_simple(1),
        fetch_user_simple(2),
        fetch_user_simple(3),
        fetch_user_order("A", 2),
        fetch_user_order("B", 1),
        fetch_user_order("C", 3),
    )
    print(result)

asyncio.run(main())