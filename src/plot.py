import matplotlib.pyplot as plt

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
