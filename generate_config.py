import configparser
import platform
import os

config_file = 'config.cfg'

# because windows is dumb, this has to be done
system = platform.system()
if system == 'Windows':
    path = os.environ['APPDATA'] + '\\feh_bot'
else:
    # using an absolute path in linux was running into several permission errors
    pwd = 'data'

config = configparser.ConfigParser()

config['Twitter API Keys'] =  {'access secret': 0, 'access token': 0, 'consumer secret': 0, 'consumer key': 0}

config['Telegram API Keys'] = {'key': 0}

config['Data Storage Directory'] = {'dir': path}

with open(config_file, 'w') as configFile:
    config.write(configFile)
