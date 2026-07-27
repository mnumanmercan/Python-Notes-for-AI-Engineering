from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Users API")


# --- Pydantic modelleri (JS'teki "interface + Zod" karşılığı) ---

class UserIn(BaseModel):
    """İstemciden GELEN veri — yeni kullanıcı oluştururken."""
    name: str
    age: int
    email: str | None = None


class UserOut(UserIn):
    """İstemciye DÖNEN veri — UserIn'in id eklenmiş hali (miras alıyor)."""
    id: int


# --- Sahte veritabanı (basitlik için hafızada bir liste) ---

users: list[UserOut] = [
    UserOut(id=1, name="Ada", age=30, email="ada@mail.com"),
    UserOut(id=2, name="Ben", age=25, email=None),
]


# --- Route'lar ---

@app.get("/")
def root():
    return {"message": "API çalışıyor"}


@app.get("/users")
def list_users(min_age: int = Query(0)):
    # Örnek istek:  GET /users?min_age=26   → query parametresi
    return [u for u in users if u.age >= min_age]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    # Örnek istek:  GET /users/1            → path parametresi
    for u in users:
        if u.id == user_id:
            return u
    raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")


@app.post("/users", status_code=201)
def create_user(user: UserIn):
    # Gelen JSON otomatik doğrulanıp UserIn'e çevrilir.
    new_id = max((u.id for u in users), default=0) + 1
    created = UserOut(id=new_id, **user.model_dump())
    users.append(created)
    return created