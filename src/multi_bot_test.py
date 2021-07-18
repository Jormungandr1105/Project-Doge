#/usr/bin/python3
from multi_bot import *

def load_files(coins, days):
	coin_files_list = []
	for coin in coins:
		files = []
		for day in days:
			files.append("../{0}_price_history/{1}.csv".format(coin,day))
		coin_files_list.append(files)
	return coin_files_list


def run():
	coins = ["bitcoin", "dogecoin", "ethereum", "kusama", "litecoin", "polkadot", "tron"]
	days = ["176", "177", "178", "179", "180", "181", "182", "183", "184", "185", "186", "187", "188", "189", "190", "191", "192"]
	first_half = ["167", "168", "169"]
	second_half = ["170", "171", "172"]
	alt_days = ["176", "177"]
	coin_files_list = load_files(coins, days)

	datasets = plot.setup_multiplot(coin_files_list)
	prices,times,percs,avgs,perc_avgs= plot.multi_plot_calcs(datasets, 150)
	coin_stuff = []
	#'''
	coin_stuff.append(["XBT", .001])
	coin_stuff.append(["XDG", 3.0])
	coin_stuff.append(["ETH", .0005])
	coin_stuff.append(["KUS", .100])
	coin_stuff.append(["LIT", .200])
	coin_stuff.append(["POK", .100])
	coin_stuff.append(["TRN", 99.0])
	'''
	coin_stuff.append(["XBT", 0.0])
	coin_stuff.append(["XDG", 100.0])
	coin_stuff.append(["ETH", .000])
	coin_stuff.append(["KUS", .00])
	coin_stuff.append(["LIT", .00])
	coin_stuff.append(["POK", .00])
	coin_stuff.append(["TRN", 0.0])
	'''
	bot = MultiBot(coin_stuff, 0.0046)
	bot.run_sim(prices, percs, perc_avgs)


if __name__ == '__main__':
	run()