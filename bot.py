import telegram
import telegram.ext as ext
import logging
import tweepy

# list of followers to keep track of (5 max?)
follow_list = []

def main():
    # set up logging
    '''
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)2 - %(message)s', 
        level=logging.INFO)
    '''

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
    '''
    username = raw_input("User to follow: ")
    print(twitter.get_user(username).id)
    follow_list = [str(twitter.get_user(username).id)]
    print(follow_list)
    '''

    # telegram bot stuff
    updater = ext.Updater(bot = telegram_bot)
    dispatcher = updater.dispatcher

    # start command
    start_handler = ext.CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # add to follower list
    add_handler = ext.CommandHandler('add', add, pass_args=True)
    dispatcher.add_handler(add_handler)

    list_handler = ext.CommandHandler('list_followed', list_followed)
    dispatcher.add_handler(list_handler)

    updater.start_polling()
    
    # creates listener and stream for inputted user
    listener = TweetStreamListener(twitter, telegram_bot)
    stream = tweepy.Stream(auth = twitter.auth, listener = listener)
    stream.filter(follow = follow_list, async=True)

# bot commands
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello! I am Feh Bot, and I follow Twitter accounts!")

# TODO: check if account is a valid twitter account
def add(bot, update, args):
    new_user = args[0]
    output_text = ""
    if(follow_list.count(new_user) < 1):
        follow_list.append(args[0])
        output_text = "Now following " + new_user + "."
    else:
        output_text = "Already following " + new_user + "."
    bot.send_message(chat_id=update.message.chat_id, text=output_text)

def list_followed(bot, update):
    output_text = "Here are the accounts I am currently following:\n"
    for index in range(0, len(follow_list)):
        if(index == len(follow_list)):
            output_text += follow_list[index]
        else:
            output_text += follow_list[index] + "\n"
    bot.send_message(chat_id=update.message.chat_id, text=output_text)

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