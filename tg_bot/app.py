import logging
import os
import sys

import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoblog.settings'

django.setup()

from app_handlers import collect_handlers
from credits import TOKEN
from telegram.ext import Updater

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    collect_handlers(dispatcher=dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
