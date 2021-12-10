from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from tg_bot.handlers.handlers_variables import (IS_AUTHORIZED,
                                                LIST_OF_ALL_COMMANDS)


def start(update: Update, context: CallbackContext):
    text = "Hi! I'm a bot, please talk to me!\n" + LIST_OF_ALL_COMMANDS
    update.message.reply_text(
        text=text
    )
    if not context.user_data.get(IS_AUTHORIZED):
        context.user_data[IS_AUTHORIZED] = False


def help_list(update: Update, context: CallbackContext):
    text = "Here a list of actions:\n" + LIST_OF_ALL_COMMANDS
    update.message.reply_text(
        text=text
    )


COMMON_HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('help', help_list),
]
