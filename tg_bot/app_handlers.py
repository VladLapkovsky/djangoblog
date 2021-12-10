from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler

from tg_bot.handlers.authorization_handlers import AUTHORIZE_HANDLERS
from tg_bot.handlers.common_handlers import COMMON_HANDLERS
from tg_bot.handlers.handlers_variables import CURRENT_ACTION
from tg_bot.handlers.post_handlers import POST_HANDLERS


def return_to_current_action(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="In return_to_current_action",
    )

    current_action = context.user_data[CURRENT_ACTION]
    return current_action


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. Use /help to get help.",
    )


HANDLERS = [
    *COMMON_HANDLERS,
    *AUTHORIZE_HANDLERS,
    *POST_HANDLERS,
    MessageHandler(Filters.text, return_to_current_action),
    MessageHandler(Filters.text, unknown),  # must be the last one
]


def collect_handlers(dispatcher):
    for handler in HANDLERS:
        dispatcher.add_handler(handler)
