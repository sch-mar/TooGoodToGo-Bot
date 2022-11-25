import logging
import logging.config
import logging.handlers
import yaml

import multiprocessing
import time

import tgtglib

if __name__ == '__main__':

    # start logger
    logging.config.dictConfig(yaml.load(open('log/log.config', 'r'), Loader=yaml.FullLoader))
    logger = logging.getLogger()
    logger.info('logger created')

    while True:
        p = multiprocessing.Process(target=tgtglib.bot, name="Bot")
        p.start()
        time.sleep(60*15)
        if p.is_alive():
            p.terminate()
        p.join()
        tgtglib.check_availability()
