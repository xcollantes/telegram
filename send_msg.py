"""Uni-directional Telegram message sender.

As opposed to listening for messages from chat. Does not take responses. Only
sends messages to a specific Telegram user or group.
"""

import asyncio
import os

from dotenv import load_dotenv

from telegram import Bot

load_dotenv()
TELEGRAM_APIKEY: str = os.environ["TELEGRAM_APIKEY"]
# Define the chat_id of the user or group you want to send the message to
TELEGRAM_ID: str = os.environ["TELEGRAM_ID"]


async def main() -> None:

    bot = Bot(token=TELEGRAM_APIKEY)

    # Send the message
    await bot.send_message(
        chat_id=TELEGRAM_ID, text="Hello! This is an arbitrary message."
    )

    print(f"Message sent to chat_id: {TELEGRAM_ID}")


if __name__ == "__main__":
    asyncio.run(main())
