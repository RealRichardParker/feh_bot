import requests
import tweepy


def get_updates(input):
    response = requests.get(input + 'getUpdates')
    return response

def main():
    #get key for telegram
    telegram = 'https://api.telegram.org/bot'
    key = open("API key.txt", "r")
    telegram += key.readline()

    #get keys for twitter
    consumer_key = key.readline()
    secret_key = key.readline()
    auth = tweepy.OAuthHandler(consumer_key, secret_key)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print("Error! Failed to get request token")

    #TODO: figure out wth is going on
    auth.request_token = { 'oauth_token' : token,'oauth_token_secret' : verifier }
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    #start doing cool stuff
    getUpdates = get_updates(telegram)
    print(getUpdates)

if __name__ == "__main__":
    main()