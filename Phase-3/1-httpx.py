import httpx
import asyncio

users: list[str] = ["mnumanmercan", "torvalds", "gvanrossum", "octocat"]

async def fetch_user(username: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/users/{username}"
        response = await client.get(url)
        response.raise_for_status()

        data = response.json()
        return data

async def fetch_many_user(usernames: list[str]) -> list[dict]:
    coroutines = [fetch_user(username) for username in usernames]
    result = await asyncio.gather(*coroutines)

    return result

result = asyncio.run(fetch_many_user(users))
print(result)