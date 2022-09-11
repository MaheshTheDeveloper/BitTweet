import datetime
from time import sleep

import requests
import schedule
import tweepy

# Sleep time in seconds
sleep_time: int = 10

# Tweet by price change value
tweet_by_price_change: int = 100

# Set time for good morning tweet in 24-hour format
time = "09:00"

# Which coin to track. For example: BTCUSDT or ETHUSDT. !!Don't change the 0 in the end!! It's the starting price.
dictcoins = {'BTCUSDT': 0, 'ETHUSDT': 0, }

# Consumer keys and access tokens, used for OAuth
CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'

# For in coin in dictcoins do:
for coin in dictcoins:
    # Get current price
    price = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + coin).json()['price']
    # Set current price as old price
    dict = {coin: price}
    dictcoins.update(dict)
    # Print starting the bot with the current price
    print("\033[95m" + "Started the bot for " + coin + " with price: $" + str(
        dictcoins[coin]) + "Press CTRL+C to exit" + "\033[0m")

print("\033[95m" + "The bot will check the prices every " + str(sleep_time) + " seconds \033[0m")
print("\033[95m" + f"The bot will tweet if the price changes by ${tweet_by_price_change} or more \033[0m")
print("\033[95m" + "The bot will tweet a good morning tweet at " + time + " \033[0m")


# Send a good morning tweet at 9:00
def job():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status("Good morning! The current prices are: $" + str(list(dictcoins.values())))
    print("\033[92m" + "Good morning tweet sent! \033[0m")


schedule.every().day.at(time).do(job)
while True:
    print("\033[94m" + "Checking prices... \033[0m")
    for coin in dictcoins:
        bitcoin_api_url: str = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}"
        response = requests.get(bitcoin_api_url)
        data = response.json()
        price = data["price"]
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        difference = float(price) - float(dictcoins[coin])
        print(
            "\033[92m" + f"{now} - {coin} - Current price: ${price} - Old price: ${dictcoins[coin]} - Difference: ${difference} \033[0m")
        if difference >= tweet_by_price_change:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api = tweepy.API(auth)
            api.update_status(f"{coin} price has increased by ${difference}! Current price: ${price}")
            print("\033[92m" + f"{coin} price has increased by ${difference}! Current price: ${price} \033[0m")
            dict = {coin: price}
            dictcoins.update(dict)
        elif difference <= -tweet_by_price_change:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api = tweepy.API(auth)
            api.update_status(f"{coin} price has decreased by ${difference}! Current price: ${price}")
            print("\033[92m" + f"{coin} price has decreased by ${difference}! Current price: ${price} \033[0m")
            dict = {coin: price}
            dictcoins.update(dict)

    sleep(sleep_time)
