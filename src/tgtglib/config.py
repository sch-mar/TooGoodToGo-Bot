import configparser

PATH = "config/.config"

# get value from config
def get_config(section, option, fallback = None):
    config = configparser.ConfigParser()
    config.read(PATH)
    return config.get(section, option, fallback=fallback) # fallback if no chat_ids

# change or add option in config
def set_config(section, option, value):
    config = configparser.ConfigParser()
    config.read(PATH)
    if section not in config:
        config[section] = {}
    config[section][option] = value
    config.write(open(PATH, 'w'))

# remove section or option from config
def rm_config(section, option=None):
    config = configparser.ConfigParser()
    config.read(PATH)
    if option == None:
        config.remove_section(section)
    else:
        config.remove_option(section, option)
    config.write(open(PATH, 'w'))
