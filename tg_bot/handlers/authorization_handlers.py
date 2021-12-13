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


def end_conversation(update: Update, message: str) -> int:
    update.message.reply_text(message)
    return END


def confirm_action(update: Update, context: CallbackContext) -> int:
    context.user_data[IS_AUTHORIZED] = True

    message = str(
        'We are good. You are:\n'
        f'Username: {context.user_data[USERNAME]}\n'
        '\nYou can go next.\n' + LIST_OF_ALL_COMMANDS,
    )
    return end_conversation(update=update, message=message)


def create_tgbot_record(chat_id: int, user_id: int) -> None:
    tg_bot = TelegramBotChat.objects.create(telegram_chat_id=chat_id, user_id=user_id)
    tg_bot.save()


def authorization_error(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Invalid username or password.\n'
        'Please, enter a correct username and password.\n'
        'Note that both fields may be case-sensitive.\n',
    )
    return authorize(update=update, context=context)


def check_authorization_info(update: Update, context: CallbackContext) -> int:
    try:
        user = CustomUser.objects.get(username=context.user_data[USERNAME])
    except CustomUser.DoesNotExist:
        return authorization_error(update=update, context=context)

    password = context.user_data[PASSWORD]
    if not user.check_password(raw_password=password):
        return authorization_error(update=update, context=context)

    create_tgbot_record(chat_id=update.effective_chat.id, user_id=user.id)

    return confirm_action(update=update, context=context)


def adding_password(update: Update, context: CallbackContext) -> int:
    context.user_data[PASSWORD] = update.message.text
    return check_authorization_info(update=update, context=context)


def adding_username(update: Update, context: CallbackContext) -> int:
    context.user_data[USERNAME] = update.message.text

    update.message.reply_text(
        'Please, enter your password.\n'
        'To abort, simply type /stop.',
    )
    return PASSWORD


def is_user_in_db(update: Update) -> bool:
    try:
        tg_chat = TelegramBotChat.objects.get(telegram_chat_id=update.effective_chat.id)
    except TelegramBotChat.DoesNotExist:
        tg_chat = None
    return bool(tg_chat)


def start_authorization(update: Update, context: CallbackContext) -> int:
    if is_user_in_db(update=update):
        context.user_data[IS_AUTHORIZED] = True
        message = 'You are authorized.'
        return end_conversation(update=update, message=message)

    context.user_data[IS_AUTHORIZED] = False
    update.message.reply_text(
        'Please, enter your username.\n'
        'To abort, simply type /stop.',
    )
    return USERNAME


def authorize(update: Update, context: CallbackContext) -> int:
    context.user_data[CURRENT_ACTION] = 'authorization'
    return start_authorization(update=update, context=context)


def stop_conversation(update: Update, context: CallbackContext) -> int:
    current_action = context.user_data[CURRENT_ACTION].capitalize()
    message = f'{current_action} is canceled.\n' + LIST_OF_ALL_COMMANDS
    return end_conversation(update=update, message=message)


def non_support_commands_interception(update: Update, context: CallbackContext) -> int:
    current_action = context.user_data[CURRENT_ACTION].capitalize()
    message = str(
        'Sorry, you had to not use commands.\n'
        f'{current_action} is stopped.\n'
        'Use:\n' + LIST_OF_ALL_COMMANDS,
    )
    return end_conversation(update=update, message=message)


def authorization_required(func):
    @functools.wraps(func)
    def check_is_authorized(*args, **kwargs):
        update = args[0]
        context = args[1]
        if context.user_data.get(IS_AUTHORIZED):
            return func(*args, **kwargs)
        update.message.reply_text(
            'You must be authorized to run this command.\nUse /authorize.',
        )
        return None

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
