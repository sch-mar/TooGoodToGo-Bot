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

    @bot.message_handler(commands=["start"])
    def start(message):
        # current chat id
        USER_ID = str(message.chat.id)
        # get existing users
        if jsondb.select_possible(USERDB, USER_ID):
            user_ids = [user for user in jsondb.selectall(USERDB)]
        else:
            user_ids = []
        # add new user if necessary
        if USER_ID not in user_ids: # new user
            logging.warning(f"new user: {USER_ID}")
            jsondb.insert(USERDB, USER_ID, {'name': message.chat.first_name, 'signuptime': str(datetime.now())})
            bot.send_message(USER_ID, config.get(['messages', 'welcome'], dir=MSGDIR))
            bot.register_next_step_handler_by_chat_id(int(USER_ID), mailhandler)
        else:
            logging.info(f"user {USER_ID} already configured")
            bot.send_message(USER_ID, config.get(['messages', 'nth_welcome'], dir=MSGDIR).format(jsondb.select(USERDB, 'name', message.chat.id)))

    # message catchall
    @bot.message_handler(func=lambda message: True)
    def catchall(message):
        logging.info(f"catchall message from {message.chat.id}")
        logging.debug(message)
        bot.send_message(message.chat.id, config.get(['messages', 'catchall'], dir=MSGDIR))

    # other handlers
    def mailhandler(message):
        mail_pattern = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
        if mail_pattern.match(message.text):
            logging.info(f"starting get_credentials")
            bot.send_message(message.chat.id, config.get(['messages', 'open_link'], dir=MSGDIR).format(message.text))
            tgtg.get_credentials(message.text, message.chat.id)
            logging.info(f"finished get_credentials")
            bot.send_message(message.chat.id, config.get(['messages', 'login_success'], dir=MSGDIR))
        else:
            bot.send_message(message.chat.id, config.get(['messages', 'invalid_mail'], dir=MSGDIR))
            bot.register_next_step_handler_by_chat_id(int(message.chat.id), mailhandler)
    
    #bot.infinity_polling()
    bot.polling()
