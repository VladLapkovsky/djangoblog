import functools

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler)

from tg_bot.handlers.handlers_variables import (CURRENT_ACTION, END,
                                                IS_AUTHORIZED,
                                                LIST_OF_ALL_COMMANDS, PASSWORD,
                                                USERNAME)
from tg_bot.models import TelegramBotChat
from users.models import CustomUser


def end_conversation(update: Update, message: str):
    update.message.reply_text(message)
    return END


def confirm_action(update: Update, context: CallbackContext):
    context.user_data[IS_AUTHORIZED] = True

    message = str(
        'We are good. You are:\n'
        f'Username: {context.user_data[USERNAME]}\n'
        '\nYou can go next.\n' + LIST_OF_ALL_COMMANDS
    )
    return end_conversation(update, message=message)


def create_tgbot_record(chat_id, user_id) -> None:
    tg_bot = TelegramBotChat.objects.create(telegram_chat_id=chat_id, user_id=user_id)
    tg_bot.save()
    return


def authorization_error(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Invalid username or password.\n'
        'Please, enter a correct username and password.\n'
        'Note that both fields may be case-sensitive.\n'
    )
    return authorize(update, context)


def check_authorization_info(update: Update, context: CallbackContext):
    try:
        user = CustomUser.objects.get(username=context.user_data[USERNAME])
    except CustomUser.DoesNotExist:
        return authorization_error(update, context)

    password = context.user_data[PASSWORD]
    if not user.check_password(password):
        return authorization_error(update, context)

    create_tgbot_record(chat_id=update.effective_chat.id, user_id=user.id)

    return confirm_action(update, context)


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
        message = 'You are authorized.'
        return end_conversation(update, message=message)

    context.user_data[IS_AUTHORIZED] = False
    update.message.reply_text(
        'Please, enter your username.\n'
        'To abort, simply type /stop.'
    )
    return USERNAME


def authorize(update: Update, context: CallbackContext):
    context.user_data[CURRENT_ACTION] = 'authorization'
    return start_authorization(update, context)


def stop_conversation(update: Update, context: CallbackContext) -> str:
    """Completely end conversation from within nested conversation."""

    message = f'{context.user_data[CURRENT_ACTION].capitalize()} is canceled.\n' + LIST_OF_ALL_COMMANDS
    return end_conversation(update, message=message)


def non_support_commands_interception(update: Update, context: CallbackContext):
    message = str(
        'Sorry, you had to not use commands.\n'
        f'{context.user_data[CURRENT_ACTION].capitalize()} is stopped.\n'
        'Use:\n' + LIST_OF_ALL_COMMANDS
    )
    return end_conversation(update, message=message)


def authorization_required(func):
    @functools.wraps(func)
    def check_is_authorized(*args, **kwargs):
        update = args[0]
        context = args[1]
        if not context.user_data.get(IS_AUTHORIZED):
            update.message.reply_text(
                'You must be authorized to run this command.\n'
                'Use /authorize.'
            )
            return
        else:
            res = func(*args, **kwargs)
            return res

    return check_is_authorized


AUTH_HANDLERS = [
    ConversationHandler(
        entry_points=[CommandHandler('authorize', authorize)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, adding_username)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, adding_password)],
        },
        fallbacks=[
            CommandHandler('stop', stop_conversation),
            MessageHandler(Filters.command, non_support_commands_interception),
        ],
        allow_reentry=True,
    ),
]
