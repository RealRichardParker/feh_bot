import ConfigParser

config = ConfigParser.RawConfigParser()

config.add_section('Twitter API Keys')
config.set('Twitter API Keys', 'access secret', 0)
config.set('Twitter API Keys', 'access token', 0)
config.set('Twitter API Keys', 'consumer secret', 0)
config.set('Twitter API Keys', 'consumer key', 0)

config.add_section('Telegram API Keys')
config.set('Telegram API Keys', 'key', 0)

with open('config.cfg', 'wb') as configFile:
    config.write(configFile)