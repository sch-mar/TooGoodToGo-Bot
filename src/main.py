import logging
import logging.config
import logging.handlers
import yaml

import multiprocessing
import time

from tgtglib import bot
from tgtglib import tgtg

import random

# start logger
logging.config.dictConfig(yaml.load(open('log/.config', 'r', encoding='utf8'), Loader=yaml.FullLoader))

if __name__ == '__main__':
    logging.info('program start')
    while True:
        p = multiprocessing.Process(target=bot.bot, name="Bot")
        p.start()
        time.sleep(60 * 10 + random.random() * 10 * 60)
        if p.is_alive():
            p.terminate()
        p.join()
        tgtg.check_availability()
