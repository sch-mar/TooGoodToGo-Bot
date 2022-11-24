import os.path
import telebot

import ast
import configparser
from tgtg import TgtgClient
import json

# get value from config
def get_config(section, option, fallback = None):
    config = configparser.ConfigParser()
    config.read('.config')
    return config.get(section, option, fallback=fallback) # fallback if no chat_ids

# change or add option in config
def set_config(section, option, value):
    config = configparser.ConfigParser()
    config.read('.config')
    if section not in config:
        config[section] = {}
    config[section][option] = value
    config.write(open('.config', 'w'))

# remove section or option from config
def rm_config(section, option=None):
    config = configparser.ConfigParser()
    config.read('.config')
    if option == None:
        config.remove_section(section)
    else:
        config.remove_option(section, option)
    config.write(open('.config', 'w'))

# --------------------------------------------------

def bot():
    API_KEY = get_config('telegram', 'api_key')
    bot = telebot.TeleBot(API_KEY)

    @bot.message_handler(commands=["start"])
    def start(message):
        # current chat id
        CHAT_ID = message.chat.id
        bot.send_message(CHAT_ID, "Welcome!")
        # add chat id to exisiting chat ids
        if get_config('telegram', 'chat_ids', '') == '':
            chat_ids = []
        else:
            chat_ids = get_config('telegram', 'chat_ids', '').split(',') # get chat ids
        CHAT_ID = str(CHAT_ID) # int to str
        if CHAT_ID not in chat_ids:
            chat_ids.append(CHAT_ID)
        set_config('telegram', 'chat_ids', ','.join(chat_ids))

    #bot.infinity_polling()
    bot.polling()

def check_availability():
    # read credentials
    # credentials = dict(ast.literal_eval(open("credentials", 'r').read()))
    ACCESS_TOKEN = get_config('tgtg', 'access_token')
    REFRESH_TOKEN = get_config('tgtg', 'refresh_token')
    USER_ID = get_config('tgtg', 'user_id')

    # client
    client = TgtgClient(access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, user_id=USER_ID)

    # items
    items = client.get_items()
    #print(items, file=open('items', 'w'))

    # build dict store_id: available and dict store_id: store_name
    available = {}
    stores = {}
    for group in items:
        store_id = group['store']['store_id']
        store_name = group['store']['store_name']
        items_available = group['items_available']
        available[store_id] = items_available # dict
        stores[store_id] = store_name
        #print(f"{items_available : <2} available at {store_name} ({store_id})")

    # compare new availability with cache
    if os.path.isfile('item_cache.json'):
        item_cache = json.load(open('item_cache.json', 'r'))
        for id in available:
            if id in item_cache and item_cache[id] == 0 and available[id] > 0:
                print("something is available at", stores[id])
                API_KEY = get_config('telegram', 'api_key')
                bot = telebot.TeleBot(API_KEY)
                chat_ids = get_config('telegram', 'chat_ids').split(',') # get chat ids
                for chat_id in chat_ids:
                    bot.send_message(chat_id, f"Something is available at {stores[id]}")
        print("nothing else is available")

    # cache dict locally
    json.dump(available, open('item_cache.json', 'w'))
