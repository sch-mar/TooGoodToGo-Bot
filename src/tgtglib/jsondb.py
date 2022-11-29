import os
import logging
import json

# only for 2D-files

def check_dir(dir):
    if not os.path.isdir(dir):
        logging.debug(f"creating directory {dir}")
        os.makedirs(dir)

def file_exists(path):
    return os.path.isfile(path)

def create_file(path): # means file
    logging.debug(f"creating file {path}")
    open(path, 'w').write("{}")

def insert(dir, file, key, value, section=None):
    path = dir.removesuffix('/') + '/' + file
    check_dir(dir)
    if not file_exists(path):
        create_file(path)
    cache = json.load(open(path, 'r'))
    if section:
        if section not in cache:
            cache[section] = {key: value} # creates new section
        else:
            cache[section][key] = value # adds to existing section
    else:
        cache[key] = value
    open(path, 'w').write(json.dumps(cache, indent=4))

def recreate(dir, file, data={}):
    path = dir.removesuffix('/') + '/' + file
    json.dump(data, open(path, 'w'), indent=4)


def select(dir, file, key, section=None):
    path = dir.removesuffix('/') + '/' + file
    if not os.path.isfile(path):
        logging.warning(f"File {path} does not exist. Nothing selected.") # TODO: throw error
        return False
    cache = json.load(open(path, 'r'))
    if section:
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

def selectall(dir, file):
    path = dir.removesuffix('/') + '/' + file
    if not os.path.isfile(path):
        logging.warning(f"File {path} does not exist. Nothing selected.")
        return False
    return json.load(open(path, 'r'))