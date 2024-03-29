import logging
import logging.config
import logging.handlers
import multiprocessing
import random
import time

import yaml

from tgtglib import bot, cookie, tgtg

# start logger
logging.config.dictConfig(
    yaml.load(open('log/.config', 'r', encoding='utf8'), Loader=yaml.FullLoader))

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
        try:
            tgtg.check_availability()
        except Exception as e:
            logging.warning(f"Exception while checking availability: {e}")
