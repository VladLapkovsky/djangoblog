import requests
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

URL = 'http://127.0.0.1:8000/api/posts/'


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


POST_HANDLERS = [
    CommandHandler('get_posts_count', get_posts_count),
]
