import logging
import telebot
from tgtglib import config
from tgtglib import jsondb
from tgtglib import tgtg
from datetime import datetime
import re

def bot():
    logging.debug("starting bot")
    bot = telebot.TeleBot(config.get(['telegram', 'api_key']))

    USERDB = config.get(['filenames', 'userdb'], dir='data')
    MSGDIR = 'data'
    languages = [language for language in config.get(['languages'], MSGDIR)]
    language_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for language in languages:
        language_markup.row(telebot.types.KeyboardButton(config.get(['languages', language], MSGDIR)))

    @bot.message_handler(commands=["start"])
    def start(message):
        # current chat id
        USER_ID = str(message.chat.id)
        USER_LANG = jsondb.select('users.json', 'language', USER_ID)
        # get existing users
        if jsondb.select_possible(USERDB, USER_ID):
            user_ids = [user for user in jsondb.selectall(USERDB)]
        else:
            user_ids = []
        # add new user if necessary
        if USER_ID not in user_ids: # new user
            logging.warning(f"new user: {USER_ID}")
            jsondb.insert(USERDB, USER_ID, {'name': message.chat.first_name, 'signuptime': str(datetime.now())})
            bot.send_message(USER_ID, '\n'.join([config.get(['messages', l, 'choose_language'], MSGDIR) for l in languages]), reply_markup=language_markup)
            bot.register_next_step_handler_by_chat_id(int(USER_ID), language_handler)
        else:
            logging.warning(f"user {USER_ID} already configured")
            bot.send_message(USER_ID, config.get(['messages', USER_LANG, 'nth_welcome'], dir=MSGDIR).format(jsondb.select(USERDB, 'name', USER_ID)))

    # message catchall
    @bot.message_handler(func=lambda message: True)
    def catchall(message):
        USER_ID = message.chat.id
        USER_LANG = jsondb.select('users.json', 'language', USER_ID)
        logging.info(f"catchall message from {USER_ID}")
        logging.debug(message)
        bot.send_message(USER_ID, config.get(['messages', USER_LANG, 'catchall'], dir=MSGDIR))

    # other handlers
    def mail_handler(message):
        USER_ID = message.chat.id
        USER_LANG = jsondb.select('users.json', 'language', USER_ID)
        mail_pattern = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
        if mail_pattern.match(message.text):
            logging.info(f"starting get_credentials")
            bot.send_message(USER_ID, config.get(['messages', USER_LANG, 'open_link'], dir=MSGDIR).format(message.text))
            tgtg.get_credentials(message.text, USER_ID)
            logging.info(f"finished get_credentials")
            bot.send_message(USER_ID, config.get(['messages', USER_LANG, 'login_success'], dir=MSGDIR))
        else:
            bot.send_message(USER_ID, config.get(['messages', USER_LANG, 'invalid_mail'], dir=MSGDIR))
            bot.register_next_step_handler_by_chat_id(int(USER_ID), mail_handler)
    
    def language_handler(message):
        USER_ID = message.chat.id
        lang_dict = {config.get(['languages', l], MSGDIR): l for l in [language for language in languages]}
        USER_LANG = lang_dict.get(message.text)
        logging.info(f"saving language '{USER_LANG}")
        jsondb.insert('users.json', 'language', USER_LANG, USER_ID)
        bot.send_message(USER_ID, config.get(['messages', USER_LANG, 'get_mail'], dir=MSGDIR))
        bot.register_next_step_handler_by_chat_id(int(USER_ID), mail_handler)

    
    #bot.infinity_polling()
    bot.polling()
