from fastapi import FastAPI, HTTPException

app = FastAPI()

fake_users = {
    1: {"name": "Alice", "age": 30},
    2: {"name": "Bob", "age": 25},
}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = fake_users.get(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")
