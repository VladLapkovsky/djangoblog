from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler)

from tg_bot.handlers.handlers_variables import (END, IS_AUTHORIZED,
                                                LIST_OF_ALL_COMMANDS, PASSWORD,
                                                USERNAME, CURRENT_ACTION, AUTHORIZATION, REGISTER)
from tg_bot.models import TelegramBotChat
from users.models import CustomUser


def confirm_authorization(update: Update, context: CallbackContext):
    update.message.reply_text(
        'We are good. You are:\n'
        f'Username: {context.user_data[USERNAME]}\n'
        '\nYou can go next.\n' + LIST_OF_ALL_COMMANDS
    )
    context.user_data[IS_AUTHORIZED] = True
    return END


def authorization_error(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Invalid username or password.\n'
        'Please, enter a correct username and password.\n'
        'Note that both fields may be case-sensitive.\n'
    )
    return start_authorization(update, context)


def check_authorization_info(update: Update, context: CallbackContext):
    try:
        user = CustomUser.objects.get(username=context.user_data[USERNAME])
    except CustomUser.DoesNotExist:
        return authorization_error(update, context)

    password = context.user_data[PASSWORD]
    if not user.check_password(password):
        return authorization_error(update, context)

    tg_bot = TelegramBotChat.objects.create(telegram_chat_id=update.effective_chat.id, user_id=user.id)
    tg_bot.save()
    return confirm_authorization(update, context)


def adding_password(update: Update, context: CallbackContext) -> str:
    context.user_data[PASSWORD] = update.message.text
    return check_authorization_info(update, context)


def adding_username(update: Update, context: CallbackContext) -> str:
    context.user_data[USERNAME] = update.message.text

    update.message.reply_text(
        'Please, enter your password.\n'
        'To abort, simply type /stop.'
    )
    return PASSWORD


def is_user_in_db(update: Update):
    try:
        tg_chat = TelegramBotChat.objects.get(telegram_chat_id=update.effective_chat.id)
    except TelegramBotChat.DoesNotExist:
        tg_chat = None
    return bool(tg_chat)


def start_authorization(update: Update, context: CallbackContext):
    if is_user_in_db(update):
        context.user_data[IS_AUTHORIZED] = True
        update.message.reply_text(
            'You are authorized.'
        )
        return END
    context.user_data[IS_AUTHORIZED] = False
    update.message.reply_text(
        'Please, enter your username.\n'
        'To abort, simply type /stop.'
    )
    return USERNAME


def authorize(update: Update, context: CallbackContext):
    update.message.reply_text(
        'In authorize'
    )
    context.user_data[CURRENT_ACTION] = AUTHORIZATION
    return start_authorization(update, context)


def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.\n' + LIST_OF_ALL_COMMANDS)
    return END


AUTHORIZE_HANDLERS = [
    ConversationHandler(
        entry_points=[CommandHandler('authorize', authorize)],
        states={
            AUTHORIZATION: [MessageHandler(Filters.text, authorize)],
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, adding_username)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, adding_password)],
        },
        fallbacks=[CommandHandler('stop', stop)],
    ),
    CommandHandler('stop', stop),
]