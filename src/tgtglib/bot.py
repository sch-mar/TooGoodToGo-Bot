import logging
import telebot
from tgtglib import config
from tgtglib import jsondb
from tgtglib import tgtg
from datetime import datetime
import re

def bot():
    logging.info("starting bot")
    bot = telebot.TeleBot(config.get_config('telegram', 'api_key'))

    @bot.message_handler(commands=["start"])
    def start(message):
        # current chat id
        USER_ID = str(message.chat.id)
        # get existing users
        if jsondb.select_possible('data', 'users.json', USER_ID):
            user_ids = [user for user in jsondb.selectall('data', 'users.json')]
        else:
            user_ids = []
        # add new user if necessary
        if USER_ID not in user_ids: # new user
            logging.warning(f"new user: {USER_ID}")
            jsondb.insert('data', 'users.json', USER_ID, {'name': message.chat.first_name, 'signuptime': str(datetime.now())})
            bot.send_message(USER_ID, "Welcome! Please make sure you have access to your mails either on desktop or you are able to manually open a link in a browser. If you just click the link on your mobile device, the TGTG app will open and the verification doesn't work through the app. Please provide the mail of your TGTG account:")
            bot.register_next_step_handler_by_chat_id(int(USER_ID), mailhandler)
        else:
            logging.info(f"user {USER_ID} already configured")
            bot.send_message(USER_ID, "Hi! I know you already!")

    # message catchall
    @bot.message_handler(func=lambda message: True)
    def catchall(message):
        logging.info(f"catchall message from {message.chat.id}")
        logging.debug(message)
        bot.send_message(message.chat.id, "Excuse me?")

    # other handlers
    def mailhandler(message):
        mail_pattern = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
        if mail_pattern.match(message.text):
            logging.info(f"starting get_credentials")
            bot.send_message(message.chat.id, "Please open the link and confirm the login.")
            tgtg.get_credentials(message.text, message.chat.id)
            logging.info(f"finished get_credentials")
            bot.send_message(message.chat.id, "Thank you, login succesful")
        else:
            bot.send_message(message.chat.id, "That is not a valid address, please try again.")
            bot.register_next_step_handler_by_chat_id(int(message.chat.id), mailhandler)
    
    #bot.infinity_polling()
    bot.polling()
