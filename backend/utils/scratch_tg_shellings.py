"""Отримання перших повідомлень з Telegram."""
from telethon import TelegramClient
from .secret import api_id, api_hash

client = TelegramClient('session_name', api_id, api_hash)

async def fetch_messages():
    try:
        await client.connect()
        if not client.is_connected():
            raise ConnectionError("Не вдалося підключитися до Telegram.")

        channel = '@povitryanatrivogaaa'
        all_messages = []
        limit = 50  # Отримуємо останні 50 повідомлень для ініціалізації

        async for message in client.iter_messages(channel, limit=limit):
            message_data = {
                'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                'message': message.text
            }
            all_messages.append(message_data)
        print("Перші отримані повідомлення:", all_messages)
        return all_messages
    except Exception as e:
        print(f"Помилка при отриманні перших повідомлень: {e}")
        return []
    finally:
        if client.is_connected():
            await client.disconnect()