#!/usr/bin/python3
##################
import CoinStats as CS
import time


def main():
	csg = CS.CoinStats('dogecoin')
	cse = CS.CoinStats('ethereum')
	csb = CS.CoinStats('bitcoin')
	while True:
		csg.check_price()
		cse.check_price()
		csb.check_price()
		time.sleep(1.5)


if __name__ == "__main__":
	main()