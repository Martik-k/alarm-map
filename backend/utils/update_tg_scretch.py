"""Оновлення повідомлень з Telegram."""
from telethon import TelegramClient
from datetime import datetime
from .secret import api_id, api_hash
import asyncio

client = TelegramClient('session_name', api_id, api_hash)
is_connected = False

async def connect_client():
    global is_connected
    try:
        await client.connect()
        if client.is_connected():
            is_connected = True
            print("Клієнт Telethon підключено.")
        else:
            raise ConnectionError("Не вдалося підключитися до Telegram.")
    except Exception as e:
        print(f"Помилка при підключенні клієнта Telethon: {e}")

async def disconnect_client():
    global is_connected
    if client.is_connected():
        await client.disconnect()
        is_connected = False
        print("Клієнт Telethon відключено.")

async def update_messages(last_date_str):
    global is_connected
    if not is_connected:
        await connect_client()
        if not is_connected:
            return []

    try:
        channel = '@povitryanatrivogaaa'
        new_messages = []

        if last_date_str:
            last_date = datetime.strptime(last_date_str, '%Y-%m-%d %H:%M:%S')
        else:
            last_date = None

        async for message in client.iter_messages(channel):
            if not message.text:
                continue

            msg_date = message.date.replace(tzinfo=None)
            if last_date and msg_date <= last_date:
                break

            message_data = {
                'date': msg_date.strftime('%Y-%m-%d %H:%M:%S'),
                'message': message.text
            }
            new_messages.append(message_data)

        print("Нові отримані повідомлення:", new_messages)
        return new_messages
    except Exception as e:
        print(f"Помилка при оновленні повідомлень: {e}")
        return []

# Не відключаємо клієнта тут, оскільки з'єднання має бути довготривалим