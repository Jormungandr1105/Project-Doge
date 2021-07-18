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


coin_files_list = []
coin_files_list.append(["../bitcoin_price_history/167.csv", "../bitcoin_price_history/168.csv", "../bitcoin_price_history/169.csv", "../bitcoin_price_history/170.csv", "../bitcoin_price_history/171.csv", "../bitcoin_price_history/172.csv"])
coin_files_list.append(["../dogecoin_price_history/167.csv", "../dogecoin_price_history/168.csv", "../dogecoin_price_history/169.csv", "../dogecoin_price_history/170.csv", "../dogecoin_price_history/171.csv", "../dogecoin_price_history/172.csv"])
coin_files_list.append(["../ethereum_price_history/167.csv", "../ethereum_price_history/168.csv", "../ethereum_price_history/169.csv", "../ethereum_price_history/170.csv", "../ethereum_price_history/171.csv", "../ethereum_price_history/172.csv"])
coin_files_list.append(["../kusama_price_history/167.csv", "../kusama_price_history/168.csv", "../kusama_price_history/169.csv", "../kusama_price_history/170.csv", "../kusama_price_history/171.csv", "../kusama_price_history/172.csv"])
coin_files_list.append(["../litecoin_price_history/167.csv", "../litecoin_price_history/168.csv", "../litecoin_price_history/169.csv", "../litecoin_price_history/170.csv", "../litecoin_price_history/171.csv", "../litecoin_price_history/172.csv"])
coin_files_list.append(["../polkadot_price_history/167.csv", "../polkadot_price_history/168.csv", "../polkadot_price_history/169.csv", "../polkadot_price_history/170.csv", "../polkadot_price_history/171.csv", "../polkadot_price_history/172.csv"])
coin_files_list.append(["../tron_price_history/167.csv", "../tron_price_history/168.csv", "../tron_price_history/169.csv", "../tron_price_history/170.csv", "../tron_price_history/171.csv", "../tron_price_history/172.csv"])


if __name__ == '__main__':
	#plot_buy_sell()
	datasets = plot.setup_multiplot(coin_files_list)
	plot.multi_plot(datasets, 150)