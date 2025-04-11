"""Scratch the massage and write it on json file."""
import json
from telethon import TelegramClient


api_id = "29254835"
api_hash = "1b6c249fe0616c92c24bc2c2e9854abe"
file_name = '@povitryanatrivogaaa_messages.json'

client = TelegramClient('session_name', api_id, api_hash)

async def fetch_messages():
    await client.start()
    channel = '@povitryanatrivogaaa'
    all_messages = []

    limit = 50000

    async for message in client.iter_messages(channel):
        message_data = {
            'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
            'message': message.text
        }
        all_messages.append(message_data)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(all_messages, f, ensure_ascii=False, indent=4)

    print(f'Збережено {len(all_messages)} повідомлень у файл {file_name}')

with client:
    client.loop.run_until_complete(fetch_messages())
