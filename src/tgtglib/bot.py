import logging
import re
from datetime import datetime

import telebot

from tgtglib import config, cookie, jsondb, tgtg


def bot():
    logging.debug("starting bot")

    # initiate bot
    bot = telebot.TeleBot(config.get(['telegram', 'api_key']))

    # constants
    USERDB = config.get(['filenames', 'userdb'], dir='data')
    MSGDIR = 'data'

    # language list
    languages = [language for language in config.get(['languages'], MSGDIR)]

    # language markup for set_language
    language_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for language in languages:
        language_markup.row(telebot.types.KeyboardButton(
            config.get(['languages', language], MSGDIR)))

    @bot.message_handler(commands=["start"])
    def start(message):
        # constants
        USER_ID = str(message.chat.id)
        USER_LANG = jsondb.select(USERDB, 'language', USER_ID)

        # get existing users
        if jsondb.select_possible(USERDB, USER_ID):
            user_ids = [user for user in jsondb.selectall(USERDB)]
        else:
            user_ids = []

        # check if user is existing
        if USER_ID not in user_ids:  # new user
            # set cookie to prevent main loop to from interrupting registration process
            cookie.set('registration')

            logging.warning(f"new user: {USER_ID}")

            # save user with name and time
            jsondb.insert(USERDB, USER_ID, {
                          'name': message.chat.first_name, 'signuptime': str(datetime.now())})

            # set language
            bot.send_message(USER_ID, '\n'.join([config.get(
                ['messages', l, 'choose_language'], MSGDIR) for l in languages]), reply_markup=language_markup)
            bot.register_next_step_handler_by_chat_id(
                int(USER_ID), language_handler)
        else:  # existing user
            logging.warning(f"user {USER_ID} already configured")

            bot.send_message(USER_ID, config.get(['messages', USER_LANG, 'nth_welcome'], dir=MSGDIR).format(
                jsondb.select(USERDB, 'name', USER_ID)))

    # message catchall for unhandled messages
    @bot.message_handler(func=lambda message: True)
    def catchall(message):
        # constants
        USER_ID = message.chat.id
        USER_LANG = jsondb.select(USERDB, 'language', USER_ID)

        logging.info(f"catchall message from {USER_ID}")
        logging.debug(message)

        # send message
        bot.send_message(USER_ID, config.get(
            ['messages', USER_LANG, 'catchall'], dir=MSGDIR))

    # other handlers
    def mail_handler(message):
        # constants
        USER_ID = message.chat.id
        USER_LANG = jsondb.select(USERDB, 'language', USER_ID)

        # check mail for validity
        mail_pattern = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")

        if mail_pattern.match(message.text):
            logging.info(f"starting get_credentials")

            # prompt for opening link
            bot.send_message(USER_ID, config.get(
                ['messages', USER_LANG, 'open_link'], dir=MSGDIR).format(message.text))

            # get credentials from api
            tgtg.get_credentials(message.text, USER_ID)

            logging.info(f"finished get_credentials")

            # send welcome message
            bot.send_message(USER_ID, config.get(
                ['messages', USER_LANG, 'login_success'], dir=MSGDIR))

            # remove cookie to enable main loop to resume
            cookie.rm('registration')
        else:
            # reprompt mail input
            bot.send_message(USER_ID, config.get(
                ['messages', USER_LANG, 'invalid_mail'], dir=MSGDIR))

            bot.register_next_step_handler_by_chat_id(
                int(USER_ID), mail_handler)

    def language_handler(message):
        # language dictionary
        lang_dict = {config.get(['languages', l], MSGDIR): l for l in [
            language for language in languages]}

        # constants
        USER_ID = message.chat.id
        USER_LANG = lang_dict.get(message.text)

        logging.info(f"saving language '{USER_LANG}")

        # write language to db
        jsondb.insert(USERDB, 'language', USER_LANG, USER_ID)

        # prompt for mail input
        bot.send_message(USER_ID, config.get(
            ['messages', USER_LANG, 'get_mail'], dir=MSGDIR))

        bot.register_next_step_handler_by_chat_id(int(USER_ID), mail_handler)

    # run bot
    while True:
        try:
            bot.polling()
        except Exception as e:
            logging.warning(f"Exception while polling: {e}")
