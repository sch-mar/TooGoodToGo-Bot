import logging
from tgtglib import config
from tgtg import TgtgClient
from tgtglib import jsondb
import os
import json
import telebot

def get_credentials():
    client = TgtgClient(email=config.get_config('tgtg', 'mail'))
    credentials = client.get_credentials()
    for key in credentials:
        config.set_config('tgtg', key, credentials.get(key))

def check_availability():
    logging.info("checking availabilty")
    # read credentials
    ACCESS_TOKEN = config.get_config('tgtg', 'access_token')
    REFRESH_TOKEN = config.get_config('tgtg', 'refresh_token')
    USER_ID = config.get_config('tgtg', 'user_id')
    client = TgtgClient(access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN, user_id=USER_ID)
    items = client.get_items()

    # build dicts
    available = {} # store_id: available
    stores = {} # store_id: store_name
    for group in items: # section
        store_id = group['store']['store_id']
        store_name = group['store']['store_name']
        items_available = group['items_available']
        available[store_id] = items_available # dict
        stores[store_id] = store_name
        logging.debug(f"{items_available : <2} available at {store_name} ({store_id})")

    # compare new availability with cache
    if jsondb.file_exists('data/item_cache.json'):
        # item_cache = json.load(open('data/item_cache.json', 'r'))
        item_cache = jsondb.selectall('data', 'item_cache.json')
        for id in available:
            if id in item_cache and item_cache[id] == 0 and available[id] > 0:
                logging.info("Something is available at", stores[id])
                bot = telebot.TeleBot(config.get_config('telegram', 'api_key'))
                chat_ids = config.get_config('telegram', 'chat_ids').split(',') # get chat ids
                for chat_id in chat_ids:
                    logging.info(f"sending message to {chat_id}")
                    bot.send_message(chat_id, f"Something is available at {stores[id]}.")

    # cache dict locally
    jsondb.recreate('data', 'item_cache.json', available)
