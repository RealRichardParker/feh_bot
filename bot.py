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

    #start doing cool stuff

    username = raw_input("User to follow: ")
    print(twitter.get_user(username).id)
    follow_list = [str(twitter.get_user(username).id)]
    print(follow_list)
    listener = TweetStreamListener()
    stream = tweepy.Stream(auth = twitter.auth, listener = listener)
    stream.filter(follow = follow_list)
    

class TweetStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
    
    def on_error(self, status_code):
        if status_code != 420:
            return False
        else:
            return True

if __name__ == "__main__":
    main()