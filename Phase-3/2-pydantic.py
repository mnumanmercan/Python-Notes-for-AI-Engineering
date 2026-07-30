import httpx
import asyncio
from pydantic import BaseModel

class Owner(BaseModel):
    login: str

class Repo(BaseModel):
    name: str
    stargazers_count: int
    owner: Owner
    description: str | None

async def fetch_user_repos(username: str) -> list[Repo]:
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/users/{username}/repos"
        response = await client.get(url)
        response.raise_for_status()

        data = response.json()
        return [Repo(**repo_data) for repo_data in data]

result = asyncio.run(fetch_user_repos("torvalds"))
print(result)
