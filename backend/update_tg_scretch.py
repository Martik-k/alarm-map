"""Update povitryanatrivogaaa messages with new ones from Telegram channel"""
import json
from telethon import TelegramClient
from datetime import datetime

api_id = "29254835"
api_hash = "1b6c249fe0616c92c24bc2c2e9854abe"
file_name = '@povitryanatrivogaaa_messages.json'

client = TelegramClient('session_name', api_id, api_hash)

async def update_messages():
    await client.start()
    channel = '@povitryanatrivogaaa'

    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            saved_messages = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        saved_messages = []

    if saved_messages:
        last_saved_date = max(datetime.strptime(m['date'], '%Y-%m-%d %H:%M:%S') for m in saved_messages)
    else:
        last_saved_date = None


    new_messages = []

    async for message in client.iter_messages(channel):
        if not message.text:
            continue

        msg_date = message.date.replace(tzinfo=None)
        if last_saved_date and msg_date <= last_saved_date:
            break

        message_data = {
            'date': msg_date.strftime('%Y-%m-%d %H:%M:%S'),
            'message': message.text
        }
        new_messages.append(message_data)

    if new_messages:
        updated_messages = new_messages + saved_messages
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(updated_messages, f, ensure_ascii=False, indent=4)

with client:
    client.loop.run_until_complete(update_messages())
