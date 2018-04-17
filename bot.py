import telegram
import tweepy

def main():
    # store api keys externally (not on git)
    keys = open("API key.txt", "r")

    # get telegram keys
    telegram_key = keys.readline().strip()
    telegram_bot = telegram.Bot(telegram_key)
    print(telegram_bot.get_me())

    # get keys for twitter
    consumer_key = keys.readline().strip()
    consumer_secret = keys.readline().strip()
    access_token = keys.readline().strip()
    access_secret = keys.readline().strip()

    # authorize twitter api usage
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter = tweepy.API(auth)

    # reads name of user to follow from command line
    username = raw_input("User to follow: ")
    #print(twitter.get_user(username).id)
    follow_list = [str(twitter.get_user(username).id)]
    #print(follow_list)

    # creates listener and stream for inputted user
    listener = TweetStreamListener(twitter, telegram_bot)
    stream = tweepy.Stream(auth = twitter.auth, listener = listener)
    stream.filter(follow = follow_list)

# Listener for Twitter, overrides tweepy's StreamListener to provide 
# functionality for telegram
class TweetStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        #print(status.text)
        print(self.telegram.get_me())

        # start doing cool things on update

    # On rate limit over, disconnect stream
    # else restart stream    
    def on_error(self, status_code):
        if status_code != 420:
            return False
        else:
            return True

    # Passes twitter api and telegram bot as "instance variables" (not sure 
    # what) equivalent in python is
    def __init__(self, twitter, bot):
        self.api = twitter
        self.telegram = bot
        #print(bot.get_me())

if __name__ == "__main__":
    main()