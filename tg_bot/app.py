import logging

from telegram.ext import Updater

from credits import TOKEN
from app_handlers import collect_all_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    collect_all_handlers(dispatcher=dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
