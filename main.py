import multiprocessing
import time

import tgtglib

if __name__ == '__main__':
    while True:
        p = multiprocessing.Process(target=tgtglib.bot, name="Bot")
        p.start()
        time.sleep(60*15)
        if p.is_alive():
            p.terminate()
        p.join()
        tgtglib.check_availability()
