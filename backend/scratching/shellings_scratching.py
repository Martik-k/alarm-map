"""
This module updates shelling information by fetching new messages from the '@povitryanatrivogaaa' Telegram channel.
"""

import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
from telethon import TelegramClient

load_dotenv()
API_ID_TEL = os.getenv("API_ID_TG")
API_HASH_TEL = os.getenv("API_HASH_TG")

CHANNEL = '@povitryanatrivogaaa'

async def update_messages(last_data:datetime):
    """
    Retrieves new messages from the specified Telegram channel that are newer than the given date.

    Args:
        last_data (datetime): The datetime representing the last time messages were retrieved.
                             Messages with a date equal to or older than this will be ignored.

    Returns:
        list[dict[str, datetime | str]]: A list of dictionaries, where each dictionary represents 
        a new message.
                                         Each dictionary contains the following keys:
                                         - 'date' (datetime): The datetime when the message 
                                         was sent.
                                         - 'message' (str): The text content of the message.
                                         Returns an empty list if no new messages are found.
    """
    client = TelegramClient('session_name', API_ID_TEL, API_HASH_TEL)
    await client.connect()

    new_messages = []

    async for message in client.iter_messages(CHANNEL):

        if not message.text:
            continue

        msg_date = message.date.replace(tzinfo=None)
        if msg_date <= last_data:
            break

        message_data = {
            'date': msg_date,
            'message': message.text
        }
        new_messages.append(message_data)

    await client.disconnect()
    return new_messages


def get_shellings(last_data):
    """
    Retrieves shelling information by fetching new messages from the Telegram channel
    and returns them as a list.  This function wraps the asynchronous `update_messages`
    function, running it synchronously using `asyncio.run()`.

    Args:
        last_data (datetime): The datetime representing the last time shelling
        information was retrieved.

    Returns:
        list[dict[str, datetime | str]]: A list of dictionaries, where each dictionary represents 
        a new message
                                         containing shelling information. See the `update_messages`
                                         function for the structure of the returned list and 
                                         dictionaries.
    """
    return asyncio.run(update_messages(last_data))
