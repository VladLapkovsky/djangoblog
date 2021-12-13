from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Dispatcher, Filters,
                          MessageHandler)

from tg_bot.handlers.authorization_handlers import AUTH_HANDLERS
from tg_bot.handlers.handlers_variables import IS_AUTHORIZED, LIST_OF_ALL_COMMANDS
from tg_bot.handlers.post_handlers import POST_HANDLERS
from tg_bot.handlers.registration_handlers import REG_HANDLERS


def start(update: Update, context: CallbackContext) -> None:
    text = "Hi! I'm a bot, please talk to me!\n" + LIST_OF_ALL_COMMANDS
    update.message.reply_text(
        text=text,
    )
    if not context.user_data.get(IS_AUTHORIZED):
        context.user_data[IS_AUTHORIZED] = False


def help_list(update: Update, context: CallbackContext) -> None:
    text = 'Here a list of actions:\n' + LIST_OF_ALL_COMMANDS
    update.message.reply_text(
        text=text,
    )


def unknown(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. Use /help to get help.",
    )


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help_list),
    *AUTH_HANDLERS,
    *REG_HANDLERS,
    *POST_HANDLERS,
    MessageHandler(Filters.text, unknown),  # must be the last one
]


def collect_handlers(dispatcher: Dispatcher) -> None:
    for handler in HANDLERS:
        dispatcher.add_handler(handler)
