#!/usr/bin/python3
import exchange as ex
import time


# First Pass


if __name__ == '__main__':
	key_file = "../template_keys.json"
	user_file = "../template_users.json"
	user = "user0"
	user_data = ex.get_user_info(user_file,user)
	shrimp_keys = ex.get_shrimpy_keys(key_file)
	exchange = ex.Exchange(shrimp_keys, user_data, "...")
	exchange.print_useful_info()