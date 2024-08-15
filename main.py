"""Telegram app which connects a Telegram user to a private chat with a bot."""

import logging
import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(lineno)s %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main() -> None:
    telegram_app: ApplicationBuilder = build_application(
        token=os.environ["TELEGRAM_APIKEY"]
    )

    # Command on the Telegram app is `/start`
    start_handler: CommandHandler = CommandHandler("start", start)

    telegram_app.add_handler(start_handler)

    # Start running Telegram app indefinitely and receive commands.
    telegram_app.run_polling()


def build_application(token: str) -> ApplicationBuilder:
    """Return Telegram app initialized."""
    return ApplicationBuilder().token(token).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receives a Telegram message that contains the /start command.

    Args:
        update: Contains the user message and information about who issued
            command, etc.
        context: Status of the app.
    """
    logging.info("Calling /start: update: %s context: %s", update, context.chat_data)
    logging.info("Message: %s", update.message._get_attrs())
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello {update.effective_sender.name}",
    )


if __name__ == "__main__":
    main()
