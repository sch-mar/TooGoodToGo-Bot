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
    # main loop, will only be terminated by uncatched error or other type of process termination
    while True:
        # set and start process for main bot
        p = multiprocessing.Process(target=bot.bot, name="Bot")
        p.start()
        # wait 5-15 min before checking availability
        timer = 60 * 5 + random.random() * 10 * 60
        logging.debug(f"sleeping for {timer} seconds")
        time.sleep(timer)
        # check for active registration process and wait if there is one
        while cookie.exists('registration'):
            logging.info("registration in process, waiting")
            time.sleep(10)
        # kill main bot
        if p.is_alive():
            p.terminate()
        p.join()
        # check availability
        tgtg.check_availability()
