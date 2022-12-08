import logging
import logging.config
import logging.handlers
import yaml

import multiprocessing
import time

from tgtglib import bot
from tgtglib import tgtg
from tgtglib import cookie

import random

# start logger
logging.config.dictConfig(yaml.load(open('log/.config', 'r', encoding='utf8'), Loader=yaml.FullLoader))

if __name__ == '__main__':
    logging.info('program start')
    while True:
        p = multiprocessing.Process(target=bot.bot, name="Bot")
        p.start()
        time.sleep(60 * 5 + random.random() * 10 * 60)
        # check for active registration process
        while cookie.exists('registration'):
            logging.info("registration in process, waiting")
            time.sleep(10)
        if p.is_alive():
            p.terminate()
        p.join()
        tgtg.check_availability()
