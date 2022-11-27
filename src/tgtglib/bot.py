import logging
import telebot
from tgtglib import config

def bot():
    logging.info("starting bot")
    bot = telebot.TeleBot(config.get_config('telegram', 'api_key'))

    @bot.message_handler(commands=["start"])
    def start(message):
        # current chat id
        CHAT_ID = message.chat.id
        # add chat id to exisiting chat ids
        if config.get_config('telegram', 'chat_ids', '') == '':
            chat_ids = []
        else:
            chat_ids = config.get_config('telegram', 'chat_ids', '').split(',') # get chat ids
        CHAT_ID = str(CHAT_ID) # int to str
        if CHAT_ID not in chat_ids:
            logging.info(f"new chat added: {CHAT_ID}")
            chat_ids.append(CHAT_ID)
            config.set_config('telegram', 'chat_ids', ','.join(chat_ids))
            bot.send_message(CHAT_ID, "Welcome!")
        else:
            logging.info(f"chat {CHAT_ID} already configured")
            bot.send_message(CHAT_ID, "Welcome! (again)")
    
    # message catchall
    @bot.message_handler(func=lambda m: True)
    def catchall(message):
        logging.info(f"catchall message from {message.chat.id}:")
        logging.debug(message)
        bot.send_message(message.chat.id, "Excuse me?")

    #bot.infinity_polling()
    bot.polling()
