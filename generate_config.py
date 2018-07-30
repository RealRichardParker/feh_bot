import ConfigParser
import platform

config_file = 'config2.cfg'

# because windows is dumb, this has to be done
if platform.system() == 'Windows':
    path = '\\data'
else:
    path = '/data'

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

with open(config_file, 'w') as configFile:
    config.write(configFile)
