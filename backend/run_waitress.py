import asyncio
import threading
from waitress import serve
from app import create_app
from app.shelling_updater import periodic_update
from utils import scratch_tg_shellings


app = create_app()
app.config['ALARM_DATA'] = {}


def start_flask():
    serve(app, host="0.0.0.0", port=8000)


async def get_initial_last_data():
    messages = await scratch_tg_shellings.fetch_messages()
    if messages:
        latest_message = max(messages, key=lambda x: x['date'])
        return latest_message['date']
    return None


async def start_background_tasks():
    last_data = await get_initial_last_data()
    await periodic_update(app, last_data, interval=60)  # Запускаємо й тримаємо

if __name__ == "__main__":
    # Стартуємо Flask у окремому потоці
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    # Запускаємо фоновий asyncio loop
    asyncio.run(start_background_tasks())
