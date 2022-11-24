from tgtg import TgtgClient
from tgtglib import get_config as get_config
from tgtglib import set_config as set_config

MAIL = get_config('tgtg', 'mail')
client = TgtgClient(email=MAIL)

credentials = client.get_credentials()
for key in credentials:
    set_config('tgtg', key, credentials.get(key))
