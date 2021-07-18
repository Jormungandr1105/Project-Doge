#!/usr/bin/python3
##################
import CoinStats as CS
import time


def main():
	csg = CS.CoinStats('dogecoin')
	cse = CS.CoinStats('ethereum')
	csb = CS.CoinStats('bitcoin')
	csp = CS.CoinStats("polkadot")
	csc = CS.CoinStats("cardano")
	csl = CS.CoinStats("litecoin")
	csk = CS.CoinStats('kusama')
	cst = CS.CoinStats("tron")
	coins = [csg, cse, csb, csp, csc, csl, csk, cst]
	while True:
		for coin in coins:
			coin.check_price()
		time.sleep((60/len(coins))+1)	


if __name__ == "__main__":
	main()