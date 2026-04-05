from celery import Celery
import time

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


@celery_app.task
def send_welcome_email(email: str):
    print(f"Начинаем отправку приветственного {email}...")
    time.sleep(5)
    print(f"Приветственное письмо успешно отправлено на {email}!")
    return "Success"
