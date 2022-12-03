import logging
from tgtglib import config
from tgtg import TgtgClient
from tgtglib import jsondb
import telebot

def get_credentials(email, user_id):
    client = TgtgClient(email=email)
    credentials = client.get_credentials()
    USERDB = config.get_config('DEFAULT', 'userdb', dir='data')
    for key in credentials:
        jsondb.insert(USERDB, key, credentials.get(key), user_id)

def check_availability():
    USERDB = config.get_config('DEFAULT', 'userdb', dir='data')
    MSGDB = config.get_config('DEFAULT', 'messagedb', dir='data')
    if not jsondb.selectall_possible(USERDB):
        logging.debug(f"no users registered")
        return
    users = [user for user in jsondb.selectall(USERDB)]
    if len(users) == 0:
        logging.debug(f"no users registered")
        return
    for user in users:
        logging.debug(f"checking availabilty for user {user}")
        # read credentials
        ACCESS_TOKEN = jsondb.select(USERDB, "access_token", user)
        REFRESH_TOKEN = jsondb.select(USERDB, "refresh_token", user)
        USER_ID = jsondb.select(USERDB, "user_id", user)
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
        if jsondb.select_possible(USERDB, "item_cache", user):
            item_cache = jsondb.select(USERDB, "item_cache", user)
            for id in available:
                if id in item_cache and item_cache[id] == 0 and available[id] > 0:
                    logging.info(f"Something is available at {stores[id]}")
                    bot = telebot.TeleBot(config.get_config('telegram', 'api_key'))
                    logging.info(f"sending message to {user}")
                    bot.send_message(user, jsondb.select(MSGDB, 'new_availability').format(stores[id]))

        # save available
        jsondb.insert(USERDB, "item_cache", available, user)
