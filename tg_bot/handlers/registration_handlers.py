from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler)

from tg_bot.handlers.authorization_handlers import (
    create_tgbot_record, end_conversation, is_user_in_db,
    non_support_commands_interception, stop_conversation)
from tg_bot.handlers.handlers_variables import (CURRENT_ACTION, EMAIL,
                                                IS_AUTHORIZED,
                                                LIST_OF_ALL_COMMANDS, PASSWORD,
                                                USERNAME)
from users.models import CustomUser


def confirm_register(update: Update, context: CallbackContext):
    context.user_data[IS_AUTHORIZED] = True

    message = str(
        'We are good. You are:\n'
        f'Username: {context.user_data[USERNAME]}\n'
        '\nYou can go next.\n' + LIST_OF_ALL_COMMANDS
    )
    return end_conversation(update, message=message)


def save_register_data(update: Update, context: CallbackContext):
    new_user = CustomUser.objects.create(
        username=context.user_data[USERNAME],
        email=context.user_data[EMAIL],
        password=context.user_data[PASSWORD],
    )
    new_user.save()

    create_tgbot_record(chat_id=update.effective_chat.id, user_id=new_user.id)

    return confirm_register(update, context)


def adding_password(update: Update, context: CallbackContext) -> str:
    context.user_data[PASSWORD] = update.message.text
    return save_register_data(update, context)


def password_request(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Please, enter your password.\n'
        'To abort, simply type /stop.'
    )
    return PASSWORD


def adding_email(update: Update, context: CallbackContext) -> str:
    email = update.message.text

    email_validator = EmailValidator()
    try:
        email_validator(email)
    except ValidationError as error:
        update.message.reply_text(
            f'{error.message}\n'
        )
        return email_request(update, context)

    if CustomUser.objects.filter(email=email).exists():
        update.message.reply_text(
            'The user with this email is already exists. Try another one or /authorize.\n'
        )
        return email_request(update, context)

    context.user_data[EMAIL] = email
    return password_request(update, context)


def email_request(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Please, enter your email.\n'
        'To abort, simply type /stop.'
    )
    return EMAIL


def adding_username(update: Update, context: CallbackContext) -> str:
    username = update.message.text

    username_validator = UnicodeUsernameValidator()
    try:
        username_validator(username)
    except ValidationError as error:
        update.message.reply_text(
            f'{error.message}\n'
        )
        return username_request(update, context)

    if CustomUser.objects.filter(username=username).exists():
        update.message.reply_text(
            'The user with this name is already exists. Try another one or /authorize.\n'
        )
        return username_request(update, context)

    context.user_data[USERNAME] = username
    return email_request(update, context)


def username_request(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Please, enter your username.\n'
        'To abort, simply type /stop.'
    )
    return USERNAME


def start_register(update: Update, context: CallbackContext):
    if is_user_in_db(update):
        context.user_data[IS_AUTHORIZED] = True
        message = 'You are already signed up.'
        return end_conversation(update, message=message)

    context.user_data[IS_AUTHORIZED] = False
    return username_request(update, context)


def register(update: Update, context: CallbackContext):
    context.user_data[CURRENT_ACTION] = 'registration'
    return start_register(update, context)


REG_HANDLERS = [
    ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            USERNAME: [MessageHandler(Filters.text & ~Filters.command, adding_username)],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, adding_email)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, adding_password)],
        },
        fallbacks=[
            CommandHandler('stop', stop_conversation),
            MessageHandler(Filters.command, non_support_commands_interception),
        ],
        allow_reentry=True,
    ),
]
