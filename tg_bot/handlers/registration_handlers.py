# if context.user_data[CURRENT_ACTION] == REGISTER:
#     new_user = CustomUser.objects.create(username=user.username, password=password)
#     new_user.save()
# TODO
def register(update: Update, context: CallbackContext):
    context.user_data[CURRENT_ACTION] = REGISTER
    return start_users_handling(update, context)
