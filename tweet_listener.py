import tweepy

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