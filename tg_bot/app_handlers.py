from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler

from tg_bot.handlers.authorization_handlers import AUTH_HANDLERS
from tg_bot.handlers.common_handlers import COMMON_HANDLERS
from tg_bot.handlers.handlers_variables import (IS_AUTHORIZED,
                                                LIST_OF_ALL_COMMANDS)
from tg_bot.handlers.post_handlers import POST_HANDLERS
from tg_bot.handlers.registration_handlers import REG_HANDLERS


def start(update: Update, context: CallbackContext):
    text = "Hi! I'm a bot, please talk to me!\n" + LIST_OF_ALL_COMMANDS
    update.message.reply_text(
        text=text
    )
    if not context.user_data.get(IS_AUTHORIZED):
        context.user_data[IS_AUTHORIZED] = False

#TODO remove?

# def stop(update: Update, context: CallbackContext) -> int:
#     """End Conversation by command."""
#     update.message.reply_text('Okay, bye.\n'
#                               'Type /start if you want to speak with me again.')
#     return END


def help_list(update: Update, context: CallbackContext):
    text = "Here a list of actions:\n" + LIST_OF_ALL_COMMANDS
    update.message.reply_text(
        text=text
    )


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, I didn't understand that command. Use /help to get help.",
    )


HANDLERS = [
    *COMMON_HANDLERS,
    *AUTH_HANDLERS,
    *REG_HANDLERS,
    *POST_HANDLERS,
    MessageHandler(Filters.text, unknown),  # must be the last one
]


def collect_handlers(dispatcher):
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #     states={
    #         CURRENT_ACTION: [*AUTH_HANDLERS,
    #                            *POST_HANDLERS,
    #                            *COMMON_HANDLERS,
    #                            # CommandHandler('get_posts_count', get_posts_count),
    #                            # CommandHandler('help', help_list),
    #                            ],
    #         STOPPING: [CommandHandler('start', start)],
    #     },
    #     fallbacks=[CommandHandler('stop', stop)],
    #     allow_reentry=True,
    # )
    # dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(MessageHandler(Filters.text, unknown))  # must be the last one

    for handler in HANDLERS:
        dispatcher.add_handler(handler)
