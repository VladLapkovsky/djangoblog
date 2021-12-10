from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from tg_bot.handlers.handlers_variables import SELECTING_ACTION, LIST_OF_ALL_COMMANDS


def help_list(update: Update, context: CallbackContext):
    text = "Here a list of actions:\n" + LIST_OF_ALL_COMMANDS
    update.message.reply_text(
        text=text
    )
    return SELECTING_ACTION


COMMON_HANDLERS = [
    CommandHandler('help', help_list),
]
