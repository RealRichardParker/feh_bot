import tweepy

#TODO: may need to figure out if external class can be used or not, need the list of chats and stuff

# Listener for Twitter, overrides tweepy's StreamListener to provide 
# functionality for telegram
class TweetStreamListener(tweepy.StreamListener):

    def on_data(self, status):
        #self.on_status(self, status)
        return False

    def on_status(self, status):
        #print(status.text)
        #print(self.telegram.get_me())
        for id in self.chat_map[status.author]:
            self.telegram.send_message(id, status.text)

        # start doing cool things on update

    # On rate limit over, disconnect stream
    # else restart stream    
    def on_error(self, status_code):
        if status_code != 420:
            return False
        else:
            return True

    #may not need
    def update_listener(self, account):
        self.chat_map.append(account)

    # Passes twitter api and telegram bot as "instance variables" (not sure 
    # what) equivalent in python is
    def __init__(self, twitter, bot, chat_map):
        self.api = twitter
        self.telegram = bot
        self.chat_map = chat_map
        #print(bot.get_me())