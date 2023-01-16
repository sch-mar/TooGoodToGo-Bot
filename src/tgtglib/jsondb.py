import json
import logging
import os

DEFAULT_DIR = 'data'

"""
only for 2D-files
"""


def check_dir(dir):
    if not os.path.isdir(dir):
        logging.debug(f"creating directory {dir}")
        os.makedirs(dir)


def file_exists(path):
    return os.path.isfile(path)


def create_file(path):
    logging.debug(f"creating file {path}")
    open(path, 'w', encoding='utf8').write("{}")


def insert(file, key, value, section=None, dir=DEFAULT_DIR):
    key = str(key)
    path = dir.removesuffix('/') + '/' + file
    check_dir(dir)
    if not file_exists(path):
        create_file(path)
    cache = json.load(open(path, 'r', encoding='utf8'))
    if section:
        section = str(section)
        if section not in cache:
            cache[section] = {key: value}  # creates new section
        else:
            cache[section][key] = value  # adds to existing section
    else:
        cache[key] = value
    open(path, 'w', encoding='utf8').write(json.dumps(cache, indent=4))


def remove(file, key, section=None, dir=DEFAULT_DIR):
    key=str(key)
    path = dir.removesuffix('/') + '/' + file
    if file_exists(path):
        cache = json.load(open(path, 'r', encoding='utf8'))
        if section:
            section = str(section)
            if section in cache:
                cache[section].pop(key, None)
                open(path, 'w', encoding='utf8').write(json.dumps(cache, indent=4))
        else:
            if key in cache:
                cache.pop(key, None)
                open(path, 'w', encoding='utf8').write(json.dumps(cache, indent=4))


def recreate(file, data={}, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/' + file
    json.dump(data, open(path, 'w', encoding='utf8'), indent=4)


def select(file, key, section=None, dir=DEFAULT_DIR):
    key = str(key)
    path = dir.removesuffix('/') + '/' + file
    if not os.path.isfile(path):
        # TODO: throw error
        logging.warning(f"File {path} does not exist. Nothing selected.")
        return False
    cache = json.load(open(path, 'r', encoding='utf8'))
    if section:
        section = str(section)
        try:
            return cache[section][key]
        except:
            logging.warning(f"Error selecting {section}.{key} in {path}")
            return False
    else:
        try:
            return cache[key]
        except:
            logging.warning(f"Error selecting {key} in {path}")
            return False


def selectall(file, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/' + file
    if not os.path.isfile(path):
        logging.warning(f"File {path} does not exist. Nothing selected.")
        return False
    return json.load(open(path, 'r', encoding='utf8'))


def select_possible(file, key, section=None, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/' + file
    if not os.path.isfile(path):
        return False
    try:
        cache = json.load(open(path, 'r', encoding='utf8'))
    except:
        return False
    if section:
        try:
            v = cache[section][key]
            return True
        except:
            return False
    else:
        try:
            v = cache[key]
            return True
        except:
            return False


def selectall_possible(file, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/' + file
    try:
        json.load(open(path, 'r', encoding='utf8'))
        return True
    except:
        return False
