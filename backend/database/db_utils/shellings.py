import asyncio
from utils import update_tg_scretch
from datetime import datetime
from ..models import db, Shelling
from flask import current_app

def process_shelling_data(shelling_data: list[dict[str, str]]):
    with current_app.app_context():
        for shelling in shelling_data:
            datetime_str = f"{shelling['date']} {shelling['time']}"
            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            new_alarm = Shelling(time=datetime_object, location=shelling['city'])
            db.session.add(new_alarm)
            db.session.commit()


async def _async_get_shelling(last_data):
    data = await update_tg_scretch.update_messages(last_data)
    if data:
        # Обробка отриманих даних (наприклад, збереження в БД)
        print("Отримано нові дані про обстріли:", data)
        with current_app.app_context():  # Створюємо контекст додатку
            process_shelling_data(data)
    else:
        print("Нових даних про обстріли немає.")

def start_async_shelling(last_data):
    asyncio.run(_async_get_shelling(last_data))
