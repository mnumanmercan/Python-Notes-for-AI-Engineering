from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI()

class GitHubUser(BaseModel):
    login: str
    name: str | None
    public_repos: int
    followers: int

async def fetch_user(username: str) -> GitHubUser:
    async with httpx.AsyncClient() as client:
        url = f"https://api.github.com/users/{username}"
        response = await client.get(url)
        response.raise_for_status()

        data = response.json()
        return GitHubUser(**data)

@app.get("/users/{username}")
async def get_user(username: str) -> GitHubUser:
    try:
        data = await fetch_user(username)
        return data
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="User not exist!")