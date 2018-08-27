import telegram
import telegram.ext as ext
import logging
import tweepy
import configparser
import tweet_listener
import os
import pickle
import signal

#TODO: store keys in env variables
#TODO: export chat_map using pickle on program exit

config_file = 'config.cfg'

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

    global chat_map 
    chat_map = dict()
    read_config()

    # set up telegram telegram bot 
    global updater
    updater = ext.Updater(bot = telegram_bot)
    dispatcher = updater.dispatcher
    init_handlers(dispatcher)
    updater.start_polling()

def read_config():
    config = configparser.ConfigParser()
    config.read(config_file)

    #global vars
    global telegram_bot
    global twitter
    global listener
    global stream

    # get telegram keys
    telegram_key = config.get('Telegram API Keys', 'key')
    telegram_bot = telegram.Bot(telegram_key)
    print(telegram_bot.get_me())

    # get keys for twitter
    consumer_key = config.get('Twitter API Keys', 'consumer key')
    consumer_secret = config.get('Twitter API Keys', 'consumer secret')
    access_token = config.get('Twitter API Keys', 'access token')
    access_secret = config.get('Twitter API Keys', 'access secret')

    # authorize twitter api usage
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter = tweepy.API(auth)

    # creates listener and stream for inputted user
    listener = tweet_listener.TweetStreamListener(twitter, telegram_bot)
    stream = tweepy.Stream(auth = twitter.auth, listener = listener)

    # reads in data from previous instance, if it exists
    global data_dir
    data_dir = config.get('Data Storage Directory', 'dir')
    if(os.path.isdir(data_dir)):
        files = os.listdir(data_dir)
        os.chdir(data_dir)
        print("attempting to load previous data...")
        is_loaded = False
        for file in files:
            if file.endswith('.pkl'):
                chat_map = pickle.load(open(file, 'rb'))
                is_loaded = True
            print(file)
        if is_loaded:
            print('previous data loaded!')
            print(chat_map)
        else:
            print("no data loaded")


# handlers for telegram commands
def init_handlers(dispatcher):

    # start command
    start_handler = ext.CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # add to follower list
    # TODO: do a thing when not given an argument 
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
    new_account = args[0]
    print(new_account)
    output_text = ""
    chat_id = update.message.chat_id
    if(new_account in chat_map):
        chats_following = chat_map[new_account]
        if(chat_id in chats_following):
            output_text = "Already follwing " + new_account + "."
        else:
            output_text = "Now following " + new_account + "."
            chats_following.add(chat_id)
    else:
        try:
            twitter.get_user(new_account)
            output_text = "Now following " + new_account + "."
        except tweepy.error.TweepError:
            output_text = "Error: " + new_account + " is not a valid Twitter account"
        bot.send_message(chat_id=update.message.chat_id, text=output_text)
        chat_map[new_account] = set([chat_id])
        listener.update_listener(new_account)
        stream.filter(listener.account_list, async=True)

    """        
    if(follow_list.count(new_account) >= 1):
        follow_list.append(args[0])
        output_text = "Already following " + new_account + "."
    else:
        try:
            twitter.get_user(new_account)
            output_text = "Now following " + new_account + "."
        except tweepy.error.TweepError:
            output_text = "Error: " + new_account + " is not a valid Twitter account"
        bot.send_message(chat_id=update.message.chat_id, text=output_text)
        stream.filter(follow = follow_list, async=True)
    """

def list_followed(bot, update):
    follow_set = set() 
    chat_id = update.message.chat_id
    for account, chat_id_list in chat_map.items():
        if(chat_id in chat_id_list):
            follow_set.add(account)
    # print("finished looking through set")

    if(len(follow_set) == 0):
        bot.send_message(chat_id=update.message.chat_id, text="I am not currently following any accounts.")
    else:
        output_text = "Here are the accounts I am currently following:"
        for account in follow_set:
                output_text += "\n@" + account
        bot.send_message(chat_id=chat_id, text=output_text)

def help(bot, update):
    help_text = "Here are the commands you can use:\n\n" \
                "/start - starts the bot in this chat\n" \
                "/follow USERNAME - adds USERNAME to the follow list\n" \
                "/list_followed - lists out which Twitter accounts I am monitoring for updates\n" \
                "/help - prints this message"
    bot.send_message(chat_id=update.message.chat_id, text=help_text)

def save_chat_map(signum, frame):
    updater.stop()
    print("feh_bot: saving chat map...")
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    os.chdir(data_dir)
    print(os.getcwd())
    pickle.dump(chat_map, open('chat_map.pkl', 'wb'))
    """
    with open('chat_map.pkl', 'wb') as file:
        pickle.dump(chat_map, file, pickle.HIGHEST_PROTOCOL)
    """
    print('feh_bot: chat map saved!')
    raise SystemExit

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, save_chat_map)
    signal.signal(signal.SIGINT, save_chat_map)
    try:
        main()
    except SystemExit:
        print("exiting program")