import configparser

DEFAULT_DIR = 'config'

"""
Hardcoded to '.config' files in different paths.
No directory/software module should need multiple
config files.
"""

# get value from config
def get_config(section, option, dir=DEFAULT_DIR, fallback=None):
    path = dir.removesuffix('/') + '/.config'
    config = configparser.ConfigParser()
    config.read(path)
    return config.get(section, option, fallback=fallback)

# change or add option in config
def set_config(section, option, value, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/.config'
    config = configparser.ConfigParser()
    config.read(path)
    if section not in config:
        config[section] = {}
    config[section][option] = value
    config.write(open(path, 'w'))

# remove section or option from config
def rm_config(section, option=None, dir=DEFAULT_DIR):
    path = dir.removesuffix('/') + '/.config'
    config = configparser.ConfigParser()
    config.read(path)
    if option == None:
        config.remove_section(section)
    else:
        config.remove_option(section, option)
    config.write(open(path, 'w'))
