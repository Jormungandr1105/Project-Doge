#!/usr/bin/python3
##################
from CoinStats import CoinStats
import plot


def plot_buy_sell():
	buy_file = "../histories/buys.csv"
	sell_file = "../histories/sells.csv"
	prices = ["../dogecoin_price_history/105.csv","../dogecoin_price_history/106.csv","../dogecoin_price_history/107.csv","../dogecoin_price_history/108.csv","../dogecoin_price_history/109.csv","../dogecoin_price_history/110.csv"]
	plot.plot_buy_sell(buy_file,sell_file,prices)


def plot_coin_history():
	currency = "ethereum"
	stats_obj = CoinStats(currency)
	filename = "123.csv"
	csv_file = "../{0}_price_history/{1}".format(currency,filename)
	stats_obj.plot_data(csv_file)



if __name__ == '__main__':
	plot_buy_sell()