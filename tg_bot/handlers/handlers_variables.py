from telegram.ext import ConversationHandler

USERNAME, PASSWORD, EMAIL, IS_AUTHORIZED = map(chr, range(4))
STOPPING, CURRENT_ACTION = map(chr, range(4, 6))

END = ConversationHandler.END

LIST_OF_ALL_COMMANDS = """
/help to get help message.

/register to register.
/authorize to authorize.

/get_posts_count to get posts count.
"""
