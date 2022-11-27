from tgtg import TgtgClient
from .. import tgtglib

MAIL = config.get_config('tgtg', 'mail')
print(MAIL)
exit()
client = TgtgClient(email=MAIL)

credentials = client.get_credentials()
for key in credentials:
    tgtglib.config.set_config('tgtg', key, credentials.get(key))
