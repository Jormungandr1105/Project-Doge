#!/usr/bin/python3

import exchange as ex
from multi_bot import *
import CoinStats as CS
import time
import json


def setup():
	key_file = "../jsons/keys.json"
	user_file = "../jsons/users.json"
	balance_file = "../jsons/exchange_balance.json"
	user = "user0"
	user_data = ex.get_user_info(user_file,user)
	shrimp_keys = ex.get_shrimpy_keys(key_file)
	EXCHANGE = ex.Exchange(shrimp_keys, user_data)
	EXCHANGE.get_balance()
	EXCHANGE.save_balance(balance_file)
	EXCHANGE.print_useful_info()
	return EXCHANGE

def main():
	EXCHANGE = setup()
	coins = ["bitcoin", "dogecoin", "ethereum", "kusama", "litecoin", "polkadot", "tron"]
	coin_symbols = ["XBT", "XDG", "ETH", "KSM", "LTC", "DOT", "TRX"]
	c_stats = CS.CoinStats(coins)

	bot = MultiBot(coins, loss=.0046, exchange=EXCHANGE)
	bot.run_real(c_stats, coin_symbols)



if __name__ == '__main__':
	main()