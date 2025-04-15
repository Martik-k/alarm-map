import asyncio
from utils import update_tg_scretch, timeframe_analitics
from database.db_utils.shellings import process_shelling_data
import threading
import time

async def _async_get_shelling(app, last_data):
    try:
        data = await update_tg_scretch.update_messages(last_data)
        if data:
            filtert_data, new_last_data = timeframe_analitics.extract_shelling_info(data)
            print('upload')
            with app.app_context():
                process_shelling_data(filtert_data)
            return new_last_data
        return last_data
    except Exception as e:
        print(f"Помилка в _async_get_shelling: {e}")
        return last_data

async def periodic_update(app, initial_last_data, interval=60):
    last_data = initial_last_data
    await update_tg_scretch.connect_client()  # Підключаємо клієнта при старті
    while True:
        try:
            updated_last_data = await _async_get_shelling(app, last_data)
            if updated_last_data:
                last_data = updated_last_data
        except Exception as e:
            print(f"Помилка в periodic_update: {e}")
        await asyncio.sleep(interval)
    await update_tg_scretch.disconnect_client() # Відключаємо клієнта при завершенні

def start_periodic_shelling(app, initial_last_data, interval=60):
    asyncio.create_task(periodic_update(app, initial_last_data, interval))