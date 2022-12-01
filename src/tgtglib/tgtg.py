import logging
from tgtglib import config
from tgtg import TgtgClient
from tgtglib import jsondb
import telebot

def get_credentials(email, user_id):
    client = TgtgClient(email=email)
    credentials = client.get_credentials()
    credentials = {"ACCESS_TOKEN": "e30.eyJzdWIiOiI4MDQzMTI1MCIsImV4cCI6MTY2OTQ4MjgzNiwidCI6IjVsSkVVa1hVUUJxejhZSjJkVXlwVkE6MDoxIn0.PmuT5lxUzKh8ObfOGliY5b0iiH4tsIOLR4DFfdDCOVI", "REFRESH_TOKEN": "e30.eyJzdWIiOiI4MDQzMTI1MCIsImV4cCI6MTcwMDg0NjAzNiwidCI6Ilpyc2cxT2xrUUZDTVZRNGF2UjkycEE6MDowIn0.Gzaz7vct7Ox-LtrcW3X0DxcgJQnXdelpPiRk1kBN34I", "USER_ID": "80431250"}
    for key in credentials:
        jsondb.insert('data', 'users.json', key, credentials.get(key), user_id)

def check_availability():
    if not jsondb.selectall_possible('data', 'users.json'):
        logging.info(f"no users registered")
        return
    users = [user for user in jsondb.selectall('data', 'users.json')]
    if len(users) == 0:
        logging.info(f"no users registered")
        return
    for user in users:
        logging.info(f"checking availabilty for user {user}")
        # read credentials
        ACCESS_TOKEN = jsondb.select('data', 'users.json', "ACCESS_TOKEN", user)
        REFRESH_TOKEN = jsondb.select('data', 'users.json', "REFRESH_TOKEN", user)
        USER_ID = jsondb.select('data', 'users.json', "USER_ID", user)
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
        if jsondb.select_possible('data', 'users.json', "item_cache", user):
            item_cache = jsondb.select('data', 'users.json', "item_cache", user)
            for id in available:
                if id in item_cache and item_cache[id] == 0 and available[id] > 0:
                    logging.info(f"Something is available at {stores[id]}")
                    bot = telebot.TeleBot(config.get_config('telegram', 'api_key'))
                    logging.info(f"sending message to {user}")
                    bot.send_message(user, f"Something is available at {stores[id]}.")

        # save available
        jsondb.insert('data', 'users.json', "item_cache", available, user)
