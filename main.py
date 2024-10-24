"""Telegram app which connects a Telegram user to a private chat with a bot."""

import logging
import os
import random
from uuid import uuid4

from dotenv import load_dotenv

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          InlineQueryHandler, MessageHandler, filters)

load_dotenv()
TELEGRAM_APIKEY: str = os.environ["TELEGRAM_APIKEY"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(lineno)s %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main() -> None:
    telegram_app: ApplicationBuilder = build_application(token=TELEGRAM_APIKEY)

    # Command on the Telegram app is `/do`
    # Texting in app `/do` will call `some_action()`
    # "Start" is not required
    some_action_handler: CommandHandler = CommandHandler("do", some_action)

    # Inline in Telegram app is `@my_bot some query`
    caps_handler: InlineQueryHandler = InlineQueryHandler(inline_caps)

    # Handler for errors and other fallback cases.
    fallback_handler: MessageHandler = MessageHandler(filters.COMMAND, fallback)

    telegram_app.add_handler(some_action_handler)
    telegram_app.add_handler(caps_handler)
    telegram_app.add_handler(fallback_handler)  # Error fallback handlers must be last.

    # Start running Telegram app indefinitely and receive commands.
    telegram_app.run_polling()


def build_application(token: str) -> ApplicationBuilder:
    """Return Telegram app initialized."""
    return ApplicationBuilder().token(token).build()


async def some_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receives a Telegram message that contains the /do command.

    Then sends a response message.

    Args:
        update: Contains the user message and information about who issued
            command, etc.
        context: Status of the app.
    """
    logging.info(
        "Calling /some_action: update: %s context: %s", update, context.chat_data
    )
    logging.info("Message: %s", update.message._get_attrs())

    logging.info("Message text: %s", update.message.text)  # /do X -> "/do X"
    logging.info("Args: %s", context.args)  # /do X -> ["X"]

    # TODO: Do some logic here.

    # Send a message to the user.
    #
    # Options: https://docs.python-telegram-bot.org/en/stable/telegram.message.html#message
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello {update.effective_sender.name}",
    )

    # `reply_text` is shortcut for `send_message` if text only.
    #
    # await update.message.reply_text("Hello, I am a bot. I can do anything.")

    # Markdown formatted messages.
    #
    # await update.message.reply_markdown("**Bold** and _italic_ ![Link](https://www.google.com)")


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for inline.

    If you want to implement inline functionality for your bot, please first
    talk to @BotFather and enable inline mode using /setinline. It sometimes
    takes a while until your Bot registers as an inline bot on your client.
    """
    query: str = update.inline_query.query
    if not query:
        return

    results: list = []
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="All caps",
            input_message_content=InputTextMessageContent(query.upper()),
        )
    )

    await context.bot.answer_inline_query(update.inline_query.id, results)


async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Catch all when command is not valid such as `/commandnotexist`."""
    responses: list[str] = ["Uh say again?", "Not a command.", "I didn't understand."]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=random.choice(responses),
    )


if __name__ == "__main__":
    main()
