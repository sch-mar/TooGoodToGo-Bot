import logging
import logging.config
import logging.handlers
import os
import sys

import telebot
import yaml

# enable import
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from tgtglib import config, jsondb


if __name__ == "__main__":
    # logging
    logging.config.dictConfig(
        yaml.load(open('log/.config', 'r', encoding='utf8'), Loader=yaml.FullLoader))
    logging.info(f"SCRIPT:deleting custom keyboards for all users")

    # bot
    bot = None

    # get users
    for user in jsondb.selectall('users.json'):
        # initialize bot
        if not bot:
            bot = telebot.TeleBot(config.get(['telegram', 'api_key']))

        logging.info(f"SCRIPT:user {user}")

        # send message
        bot.send_message(user, "Deleting custom keyboard.",
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    # terminate bot
    if bot:
        bot.close

    logging.info(f"SCRIPT:done")
