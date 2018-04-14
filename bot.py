import requests
import telegram
import tweepy

def main():
    #store api keys externally (not on git)
    keys = open("API key.txt", "r")

    #get telegram keys
    telegram_key = keys.readline().strip()
    telegram_bot = telegram.Bot(telegram_key)
    print(telegram_bot.get_me())

    #get keys for twitter
    consumer_key = keys.readline().strip()
    consumer_secret = keys.readline().strip()
    access_token = keys.readline().strip()
    access_secret = keys.readline().strip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter = tweepy.API(auth)

    twitter.update_status(status="Testing Twitter API")

    #start doing cool stuff

if __name__ == "__main__":
    main()