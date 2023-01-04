import logging

import telebot
from tgtg import TgtgClient

from tgtglib import config, jsondb


def get_credentials(email, user_id):
    # constants
    USERDB = config.get(['filenames', 'userdb'], dir='data')

    # initiate client
    client = TgtgClient(email=email)

    # get credentials
    credentials = client.get_credentials()

    # write credentials to db
    for key in credentials:
        jsondb.insert(USERDB, key, credentials.get(key), user_id)


def check_availability():
    # constants
    USERDB = config.get(['filenames', 'userdb'], dir='data')
    MSGDIR = 'data'

    # check if users exist (db exists)
    if not jsondb.selectall_possible(USERDB):
        logging.debug(f"no users registered")
        return

    # user list
    users = [user for user in jsondb.selectall(USERDB)]

    # check if users exist (users in db exist)
    if len(users) == 0:
        logging.debug(f"no users registered")
        return

    for user in users:
        # variables
        USER_LANG = jsondb.select('users.json', 'language', user)

        logging.debug(f"checking availabilty for user {user}")

        # read credentials
        ACCESS_TOKEN = jsondb.select(USERDB, "access_token", user)
        REFRESH_TOKEN = jsondb.select(USERDB, "refresh_token", user)
        USER_ID = jsondb.select(USERDB, "user_id", user)

        # initiate client
        client = TgtgClient(access_token=ACCESS_TOKEN,
                            refresh_token=REFRESH_TOKEN, user_id=USER_ID)

        # get items
        items = client.get_items()

        # parse items
        available = {}  # store_id: available
        stores = {}  # store_id: store_name
        for group in items:  # section
            store_id = group['store']['store_id']
            store_name = group['store']['store_name']

            items_available = group['items_available']

            available[store_id] = items_available
            stores[store_id] = store_name

            logging.debug(
                f"{items_available : <2} available at {store_name} ({store_id})")

        # compare new availability with cache
        if jsondb.select_possible(USERDB, "item_cache", user):
            # get item cache for user
            item_cache = jsondb.select(USERDB, "item_cache", user)

            for id in available:
                # check if id is known and availability > 0
                if id in item_cache and item_cache[id] == 0 and available[id] > 0:
                    logging.info(f"Something is available at {stores[id]}")

                    # initiate bot
                    bot = telebot.TeleBot(config.get(['telegram', 'api_key']))

                    logging.info(f"sending message to {user}")

                    # construct message depending an amount of items (singular/plural)
                    if available[id] == 1:
                        msg = config.get(
                            ['messages', USER_LANG, 'new_availability_singular'], dir=MSGDIR)
                    else:
                        msg = config.get(
                            ['messages', USER_LANG, 'new_availability_plural'], dir=MSGDIR)

                    # send message
                    bot.send_message(user, msg.format(
                        available[id], stores[id]))
                        
        # overwrite available items in db
        jsondb.insert(USERDB, "item_cache", available, user)
