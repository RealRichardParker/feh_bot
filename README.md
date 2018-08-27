# feh_bot
feh_bot is a bot that forwards tweets in real-time to Telegram group chats or individuals. Hosted on an AWS EC2 Instance

## Planned Features
* Updating chats of any missed Tweets in case of going offline 
* Maintaining data between instances

# Getting Started
## Prerequisites

Python 3.6 is required for this project, found [here](https://www.python.org/downloads/release/python-366/)

Install the python packages python-telegram-bot and tweepy

```
pip install python-telegram-bot --upgrade
pip install tweepy --upgrade
```
## Installing
Clone this repository

```
git clone https://github.com/RealRichardParker/feh_bot.git
```
Run the script generate_config.py
```
python3 generate_config.py
```
A file called config.cfg will be created, open it and replace all the 0 with the Twitter and Telegram API keys.

Twitter keys can be obtained by
1. Visiting https://apps.twitter.com/ and logging in
2. Clicking "Create App"
3. Filling out the form and agreeing to the Terms and Conditions
4. Click on “Keys and Access Tokens”. The Consumer Key and Secret are found here
5. Click on "Create my access token". The Access Token and Secret will be generated for you

Telegram API key can be obtained from the [@Botfather](https://t.me/BotFather)

# Usage
## Starting the bot
1. Add [@feh_bot](https://t.me/feh_news_bot)

2. Run the /start command

3. Start following Twitter accounts

## Commands

| Command        | Description           | Usage  |
| --- |---| ---|
| /start      | Starts the bot in the current chat | /start |
| /follow      | Follows the given Twitter account if it exists and forwards any tweets in realtime      |   /follow `<username>` |
| /list_followed | Lists any Twitter Accounts that this chat is following      |    /list_followed |
|/help | Displays a help message | /help

# Built With
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

[tweepy](http://www.tweepy.org/)

# License
This project is licensed under the MIT License - see the LICENSE.txt file for details