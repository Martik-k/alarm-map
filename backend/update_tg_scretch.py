"""Update povitryanatrivogaaa messages with new ones from Telegram channel"""
import json
from telethon import TelegramClient
from datetime import datetime
import asyncio

api_id = "28581097"
api_hash = "35d89cfcdf1d3f18c482069cb8d23478"
# api_id = "29254835"
# api_hash = "1b6c249fe0616c92c24bc2c2e9854abe"
file_name = '@povitryanatrivogaaa_messages.json'

client = TelegramClient('session_name', api_id, api_hash)

async def update_messages(last_date):
    await client.start()
    channel = '@povitryanatrivogaaa'
    last_date += ':00'
    last_date = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S")

    # try:
    #     with open(file_name, 'r', encoding='utf-8') as f:
    #         saved_messages = json.load(f)
    # except (FileNotFoundError, json.JSONDecodeError):
    #     saved_messages = []

    # if saved_messages:
    #     last_saved_date = last_data
    # else:
    #     last_saved_date = None


    new_messages = []

    async for message in client.iter_messages(channel):
        if not message.text:
            continue

        msg_date = message.date.replace(tzinfo=None)
        if msg_date <= last_date:
            break

        message_data = {
            'date': msg_date.strftime('%Y-%m-%d %H:%M:%S'),
            'message': message.text
        }
        new_messages.append(message_data)
    
    # if new_messages:
    #     updated_messages = new_messages + saved_messages
    #     return  updated_messages
        await client.disconnect()
        return new_messages

    return None
    #     with open(file_name, 'w', encoding='utf-8') as f:
    #         json.dump(updated_messages, f, ensure_ascii=False, indent=4)

# with client:
#     client.loop.run_until_complete(update_messages(last_data))

last_data = "2025-04-13 23:20:10"
def get_shelling():
    
    # last_data = datetime.strptime(last_data_str, "%Y-%m-%d %H:%M:%S")
    asyncio.run(update_messages(last_data))

# def get_shelling():
#     global last_data
#     last_data = datetime.strptime("2025-04-13 23:37:10", "%Y-%m-%d %H:%M:%S")
#     with client:
#         messege =client.loop.run_until_complete(update_messages(last_data))
#     return messege

# print(get_shelling())