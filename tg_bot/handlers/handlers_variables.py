from telegram.ext import ConversationHandler

USERNAME, PASSWORD, IS_AUTHORIZED = map(chr, range(3))
STOPPING, SELECTING_ACTION = map(chr, range(3, 5))

END = ConversationHandler.END

LIST_OF_ALL_COMMANDS = """
/help to get help message.
/authorize to authorize.
/register to register.
/get_posts_count to get posts count.
"""
