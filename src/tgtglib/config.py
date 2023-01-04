import configparser

import yaml

DEFAULT_DIR = 'config'

"""
File specification: YAML
Hardcoded to '.config' files in different paths.
No directory/software module should need multiple
config files.
"""


def get(keys: list, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/.config'
    cache = yaml.load(open(path, 'r', encoding='utf8'), Loader=yaml.FullLoader)
    for key in keys:
        cache = cache.get(key)
    if cache is not None:
        return cache
    else:
        raise KeyError


def set(keys: list, value, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/.config'
    cache = yaml.load(open(path, 'r', encoding='utf8'), Loader=yaml.FullLoader)
    try:
        sub_d = cache
        for ind, key in enumerate(keys[:-1]):
            if not ind:
                sub_d = cache.setdefault(key, {})
            else:
                sub_d = sub_d.setdefault(key, {})
        sub_d[keys[-1]] = value
    except:
        raise KeyError
    yaml.dump(cache, open(path, 'w', encoding='utf8'), yaml.Dumper)


def rm(keys: list, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/.config'
    cache = yaml.load(open(path, 'r', encoding='utf8'), Loader=yaml.FullLoader)
    try:
        sub_d = cache
        for ind, key in enumerate(keys[:-1]):
            if not ind:
                sub_d = cache.setdefault(key, {})
            else:
                sub_d = sub_d.setdefault(key, {})
        sub_d.pop(keys[-1])
    except:
        raise KeyError
    yaml.dump(cache, open(path, 'w', encoding='utf8'), yaml.Dumper)


# old functions using ini specification

# get value from config
def get_ini(section, option, dir=DEFAULT_DIR, fallback=None):
    path = dir.removesuffix('/') + '/.config'
    config = configparser.ConfigParser()
    config.read(path)
    return config.get(section, option, fallback=fallback)


# change or add option in config
def set_ini(section, option, value, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/.config'
    config = configparser.ConfigParser()
    config.read(path)
    if section not in config:
        config[section] = {}
    config[section][option] = value
    config.write(open(path, 'w', encoding='utf8'))


# remove section or option from config
def rm_ini(section, option=None, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/.config'
    config = configparser.ConfigParser()
    config.read(path)
    if option == None:
        config.remove_section(section)
    else:
        config.remove_option(section, option)
    config.write(open(path, 'w', encoding='utf8'))
