from fastapi import FastAPI, Request, HTTPException
import time
import redis
from worker import send_welcome_email

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

MAX_REQUESTS = 5
WINDOW_SECONDS = 60


def fetch_data_from_db(user_id: str):
    time.sleep(5)
    return {"user_id": user_id, "money": 10000}


@app.get("/data/{user_id}")
def get_user_data(user_id: str):
    cache_key = f"user_data:{user_id}"

    cached_data = r.get(cache_key)

    if cached_data:
        return {"source": "cache", "data": cached_data}

    db_data = fetch_data_from_db(user_id)

    r.setex(cache_key, 60, str(db_data))

    return {"source": "db", "data": db_data}


@app.get("/send_email/{email}")
def send_email(email: str):
    send_welcome_email.delay(email)
    return {"message": f"Письмо для {email} поставлено в очередь на отправку."}


@app.get("/api/data")
def get_security_date(request: Request):
    user_ip = "192.168.0.1"
    key = f"rate_limit:{user_ip}"

    current_count = r.incr(key)

    if current_count == 1:
        r.expire(key, WINDOW_SECONDS)

    if current_count > MAX_REQUESTS:
        raise HTTPException(
            status_code=429, detail="Слишком много запросов. Пожалуйста, попробуйте позже.")

    return {"data": "Здесь ваши данные.", "requests_left": MAX_REQUESTS - current_count}
