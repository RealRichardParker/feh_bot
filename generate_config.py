import ConfigParser
import platform
from os import environ

config_file = 'config.cfg'

# because windows is dumb, this has to be done
system = platform.system()
if system == 'Windows':
    path = environ['APPDATA'] + '\\feh_bot'
else:
    path = '/opt/feh_bot'

config = ConfigParser.RawConfigParser()

config.add_section('Twitter API Keys')
config.set('Twitter API Keys', 'access secret', 0)
config.set('Twitter API Keys', 'access token', 0)
config.set('Twitter API Keys', 'consumer secret', 0)
config.set('Twitter API Keys', 'consumer key', 0)

config.add_section('Telegram API Keys')
config.set('Telegram API Keys', 'key', 0)

config.add_section('Data Storage Directory')
config.set('Data Storage Directory','dir', path)

with open(config_file, 'wb') as configFile:
    config.write(configFile)
