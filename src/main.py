#!/usr/bin/python3

import exchange as ex
import Bot
import time
import json


def setup():
	key_file = "../keys.json"
	user_file = "../users.json"
	balance_file = "../exchange_balance.json"
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
	config_file = "best_fees_0052.conf"
	minimum_crypto = 50
	Bot.run_real(EXCHANGE, "dogecoin", "XDG", "../exchange_balance.json", minimum_crypto, config_file=config_file)


if __name__ == '__main__':
	main()