#!/usr/bin/python3
import exchange as ex
import time


# First Pass
def make_trade(exchange, fromSymbol, toSymbol, amt_from):
	cont = exchange.check_conversion(fromSymbol, toSymbol)
	cont = True
	if cont:
		print("Trading Pair Exists!")
		exchange.create_trade(fromSymbol,toSymbol,amt_from)
		#exchange.current_trades
		while(len(exchange.current_trades)>0):
			print(exchange.check_trades())
			time.sleep(6)

	else:
		print("Pair Doesn't Exist")
		return False


if __name__ == '__main__':
	key_file = "../jsons/keys.json"
	user_file = "../jsons/users.json"
	user = "user0"
	user_data = ex.get_user_info(user_file,user)
	shrimp_keys = ex.get_shrimpy_keys(key_file)
	exchange = ex.Exchange(shrimp_keys, user_data)
	exchange.print_useful_info()
	#make_trade(exchange,"USD","XBT", 5.00)
	