import telegram
import telegram.ext as ext
import logging
import tweepy
import ConfigParser
import tweet_listener

# TODO: parse keys from config file instead of API key.txt

# dictionary of all chats and what accounts to track
chat_map = dict()

# list of followers to keep track of (5 max?)
follow_list = []

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

# creates listener and stream for inputted user
listener = tweet_listener.TweetStreamListener(twitter, telegram_bot)
stream = tweepy.Stream(auth = twitter.auth, listener = listener)

def main():
    # set up logging
    '''
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)2 - %(message)s', 
        level=logging.INFO)
    '''
    '''
    # reads name of user to follow from command line
    username = raw_input("User to follow: ")
    print(twitter.get_user(username).id)
    follow_list = [str(twitter.get_user(username).id)]
    print(follow_list)
    '''

    # telegram bot stuff
    updater = ext.Updater(bot = telegram_bot)
    dispatcher = updater.dispatcher
    init_handlers(dispatcher)
    updater.start_polling()

# handlers for telegram commands
def init_handlers(dispatcher):

    # start command
    start_handler = ext.CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # add to follower list
    follow_handler = ext.CommandHandler('follow', follow, pass_args=True)
    dispatcher.add_handler(follow_handler)

    # list followers
    list_handler = ext.CommandHandler('list_followed', list_followed)
    dispatcher.add_handler(list_handler)

    # help command
    help_handler = ext.CommandHandler("help", help)
    dispatcher.add_handler(help_handler)

# bot commands
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hello! I am Feh Bot, and I follow Twitter accounts!")

# fafds45132 is a invalid account
def follow(bot, update, args):
    new_user = args[0]
    output_text = ""
    if(follow_list.count(new_user) >= 1):
        follow_list.append(args[0])
        output_text = "Already following " + new_user + "."
    else:
        try:
            twitter.get_user(new_user)
            output_text = "Now following " + new_user + "."
        except tweepy.error.TweepError:
            output_text = "Error: " + new_user + " is not a valid Twitter account"
        bot.send_message(chat_id=update.message.chat_id, text=output_text)
        stream.filter(follow = follow_list, async=True)

def list_followed(bot, update):
    if(len(follow_list) == 0):
        bot.send_message(chat_id=update.message.chat_id, text="I am not currently following any accounts.")
    else:
        output_text = "Here are the accounts I am currently following:\n"
        for index in range(0, len(follow_list)):
            if(index == len(follow_list)):
                output_text += follow_list[index]
            else:
                output_text += follow_list[index] + "\n"
        bot.send_message(chat_id=update.message.chat_id, text=output_text)

def help(bot, update):
    help_text = "Here are the commands you can use:\n\n" \
                "/start - starts the bot in this chat\n" \
                "/follow USERNAME - adds USERNAME to the follow list\n" \
                "/list_followed - lists out which Twitter accounts I am monitoring for updates\n" \
                "/help - prints this message"
    bot.send_message(chat_id=update.message.chat_id, text=help_text)

if __name__ == "__main__":
    main()