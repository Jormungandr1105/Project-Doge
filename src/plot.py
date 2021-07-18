import matplotlib.pyplot as plt
import statistics

def plotXvY(x,y):
	plt.plot(x,y)
	plt.xlabel("Time (s)")
	plt.ylabel("USD")
	plt.show()


def plot_buy_sell(buy_file,sell_file,price_data=None,price_path=None):
	if price_data is not None:
		times = []
		prices = []
		for fileno in range(len(price_data)):
			if price_path is not None:
				f = open(price_path+price_data[fileno])
			else:
				f = open(price_data[fileno])
			p_data = f.read()
			f.close()
			p_data = p_data.split("\n")
			for p_slice in p_data:
				if p_slice != "":
					p_slice = p_slice.split(",")
					times.append((86400.0*fileno)+float(p_slice[0]))
					prices.append(float(p_slice[1]))
		plt.plot(times,prices)
	plt.xlabel("Time (s)")
	plt.ylabel("USD")
	f = open(buy_file)
	b_data = f.read()
	f.close()
	b_data = b_data.split("\n")
	b_times = []
	b_prices = []
	for b_slice in b_data:
		if b_slice != "":
			b_slice = b_slice.split(",")
			b_times.append(float(b_slice[0]))
			b_prices.append(float(b_slice[1]))
	f = open(sell_file)
	s_data = f.read()
	f.close()
	s_data = s_data.split("\n")
	s_times = []
	s_prices = []
	for s_slice in s_data:
		if s_slice != "":
			s_slice = s_slice.split(",")
			s_times.append(float(s_slice[0]))
			s_prices.append(float(s_slice[1]))
	
	plt.scatter(b_times,b_prices,c="green")
	plt.scatter(s_times,s_prices,c="red")
	plt.show()


def setup_multiplot(coins_files_list):
	# coins_files_list orientation: list of lists of filenames by coin
	datasets =  []
	for coin in coins_files_list:
		prices = []
		times = []
		day_offset = 0
		for file in coin:
			f = open(file, "r")
			text = f.read()
			f.close()
			data = text.split("\n")
			for p_slice in data:
				if p_slice != "":
					p_slice = p_slice.split(",")
					times.append((86400.0*day_offset)+float(p_slice[0]))
					prices.append(float(p_slice[1]))
			day_offset += 1
		datasets.append([prices,times])
	return datasets


def multi_plot(datasets, increment):
	# datasets orientation: list of coins
	# coins orientation: list of [times list and prices list]
	end_indexes = [len(datasets[i][0])-1 for i in range(len(datasets))]
	times = []
	time = increment
	coins_indexes = [0 for _ in range(len(datasets))]
	coins_prices = [[] for _ in range(len(datasets))]
	while(coins_indexes != end_indexes):
		for i in range(len(datasets)):
			while (coins_indexes[i]+1 <= end_indexes[i] and datasets[i][1][coins_indexes[i]+1] < time):
				coins_indexes[i] = coins_indexes[i] + 1
			coins_prices[i].append(datasets[i][0][coins_indexes[i]])
		times.append(time)
		time += increment
	# Coins by percentage
	coins_percs = [[] for _ in range(len(coins_prices))]
	averages = [1.00]
	perc_averages = []
	for x in range(1,len(coins_prices[0])):
		for i in range(len(coins_prices)):
			coins_percs[i].append(coins_prices[i][x]/coins_prices[i][x-1])
		sum = 0
		for i in range(len(coins_percs)):
			sum += coins_percs[i][x-1]
		perc_averages.append(sum/float(len(coins_percs)))
	
	for x in range(len(perc_averages)):
		averages.append(averages[x]*perc_averages[x])
	
	# StdDev
	stddev = []
	for x in range(len(coins_percs[0])):
		stddev.append(statistics.pvariance([coins_percs[i][x] for i in range(len(coins_percs))])+1.05)

	# Plot
	for x in range(len(coins_prices)):
		plt.plot(times, coins_prices[x])
	plt.plot(times, averages)
	plt.show()
	#
	for y in range(len(coins_percs)):
		plt.plot(times[1:], coins_percs[y])
	plt.plot(times[1:], perc_averages)
	plt.plot(times[1:], stddev)
	plt.show()

def multi_plot_calcs(datasets, increment):
	# datasets orientation: list of coins
	# coins orientation: list of [times list and prices list]
	end_indexes = [len(datasets[i][0])-1 for i in range(len(datasets))]
	times = []
	time = increment
	coins_indexes = [0 for _ in range(len(datasets))]
	coins_prices = [[] for _ in range(len(datasets))]
	while(coins_indexes != end_indexes):
		for i in range(len(datasets)):
			while (coins_indexes[i]+1 <= end_indexes[i] and datasets[i][1][coins_indexes[i]+1] < time):
				coins_indexes[i] = coins_indexes[i] + 1
			coins_prices[i].append(datasets[i][0][coins_indexes[i]])
		times.append(time)
		time += increment
	# Coins by percentage
	coins_percs = [[] for _ in range(len(coins_prices))]
	for x in range(1,len(coins_prices[0])):
		for i in range(len(coins_prices)):
			coins_percs[i].append(coins_prices[i][x]/coins_prices[i][x-1])
	# Average
	averages = [1.00]
	perc_averages = []
	for x in range(1,len(coins_prices[0])):
		sum = 0
		for i in range(len(coins_percs)):
			sum += coins_percs[i][x-1]
		perc_averages.append(sum/float(len(coins_percs)))
	
	for x in range(len(perc_averages)):
		averages.append(averages[x]*perc_averages[x])

	return coins_prices, times, coins_percs, averages, perc_averages
