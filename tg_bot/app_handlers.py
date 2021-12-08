import requests
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler)

URL = 'http://127.0.0.1:8000/api/posts/'


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi! I'm a bot, please talk to me!\n"
        'Send /get_posts_count to get posts count.\n',
    )


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def get_posts_count(update: Update, context: CallbackContext):
    try:
        resp = requests.get(url=URL)
    except requests.exceptions.ConnectionError:
        msg = 'Server is temporarily unavailable.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        json_resp = resp.json()
        msg = 'Total amount of posts: ' + str(json_resp['count'])
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('get_posts_count', get_posts_count),
    MessageHandler(Filters.command, unknown),  # must be the last one
]


def collect_all_handlers(dispatcher):
    for handler in HANDLERS:
        dispatcher.add_handler(handler)
