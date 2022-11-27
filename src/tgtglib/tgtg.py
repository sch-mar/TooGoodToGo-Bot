import logging
from tgtglib import config
from tgtg import TgtgClient
import os
import json
import telebot

def check_availability():
    logging.info("checking availabilty")
    # read credentials
    ACCESS_TOKEN = config.get_config('tgtg', 'access_token')
    REFRESH_TOKEN = config.get_config('tgtg', 'refresh_token')
    USER_ID = config.get_config('tgtg', 'user_id')
    client = TgtgClient(access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, user_id=USER_ID)
    items = client.get_items()

    # build dict store_id: available and dict store_id: store_name
    available = {}
    stores = {}
    for group in items:
        store_id = group['store']['store_id']
        store_name = group['store']['store_name']
        items_available = group['items_available']
        available[store_id] = items_available # dict
        stores[store_id] = store_name
        logging.debug(f"{items_available : <2} available at {store_name} ({store_id})")

    # compare new availability with cache
    if os.path.isfile('item_cache.json'):
        item_cache = json.load(open('item_cache.json', 'r'))
        for id in available:
            if id in item_cache and item_cache[id] == 0 and available[id] > 0:
                logging.info("Something is available at", stores[id])
                bot = telebot.TeleBot(config.get_config('telegram', 'api_key'))
                chat_ids = config.get_config('telegram', 'chat_ids').split(',') # get chat ids
                for chat_id in chat_ids:
                    logging.info(f"sending message to {chat_id}")
                    bot.send_message(chat_id, f"Something is available at {stores[id]}.")

    # cache dict locally
    json.dump(available, open('item_cache.json', 'w'))
