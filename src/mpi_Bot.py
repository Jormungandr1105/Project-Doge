from mpi4py import MPI
from Bot import *
import bot_test


def mpi_train(rank, size, data_csvs, num_instances, num_gens, coin, minimum_crypto, config_file=None, fees=None):
	# Function: Trains the neural net via test_data across a number of nodes
	# Inputs:
	#		rank: MPI proc number
	# 	data_csvs: array of filenames with training data
	# 	num_instances: number of nets to test per generation
	# 	num_gens: the number of generations to run the test for
	#   coin: which crypto is being trained on
	#		minimum_crypto: least amount of crypto that can be exchanged
	# 	config_file (OPTIONAL): configuration file to start the training with
	#		fees (OPTIONAL): amount required per exchange (defaults to zero)
	#
	# Outputs:
	#		all_val: the worth of the best net generated
	#		all_net: the best net generated
	##############################################################################
	path_to_price_files = "../{}_price_history/".format(coin)
	comm = MPI.COMM_WORLD
	all_data = []
	for data_csv in data_csvs:
		f = open(path_to_price_files+data_csv)
		data = f.read()
		f.close()
		all_data.append(data)
	all_net = Bot()
	all_val = -100000
	if rank == 0:
		if config_file is not None:
			all_val, all_net = run_sim(all_data, minimum_crypto, config_file=config_file, fees=fees)
		print("STARTING UP: "+str(all_val))
	inst_val, inst_net = 0.0, Bot()
	lvl = 1.0
	for gen in range(num_gens):
		gen_net = Bot()
		gen_val = -10000000
		if rank == 0:
			data = [all_val, all_net, lvl]
		else:
			data = None
		data = comm.bcast(data, root=0)
		comm.barrier()
		all_val, all_net = data[0], data[1]
		for instance in range(math.floor(num_instances/(size))):
			if all_val <= 100.0:
				inst_val, inst_net = run_sim(all_data, minimum_crypto, fees=fees)
			else:
				delta = math.pow((rank*math.floor(num_instances/size)+instance)/float(num_instances-1),2.0)
				mod = math.sqrt(lvl)
				inst_val, inst_net = run_sim(all_data, minimum_crypto, parent=all_net, percent_d=delta*mod, fees=fees)
			if inst_val > gen_val:
				gen_val = inst_val
				gen_net = inst_net
		best = [gen_val, gen_net]
		comm.barrier()
		new_data = comm.gather(best, root=0)
		if rank == 0:
			prev_val = all_val
			for node_data in new_data:
				if node_data[0] >= all_val:
					all_val = node_data[0]
					all_net = node_data[1]
			if all_val > prev_val:
				lvl = 1.0
			else:
				lvl += 1.0
			print("BEST_OF_GEN_{}: ".format(gen)+str(all_val))
	comm.barrier()
	if rank == 0:
		print("BEST_OF_ALL: "+str(all_val))
		print(run_sim(all_data, minimum_crypto, parent=all_net, percent_d=0, fees=fees)[0])
		return all_val, all_net
	else:
		return None, None


def mpi_run_sim(data, minimum_crypto, config_file=None, parent=None, percent_d=None, fees=None):
	max_d = 24
	approx =4
	buys = []
	sells = []
	crypto_wallet = 0.0
	money = 100.00
	num_inputs = 5
	if parent is not None:
		assert(percent_d is not None)
		net = Bot(parent=parent, percent_d=percent_d, fees=fees, inputs=num_inputs)
	elif config_file is not None:
		net = Bot(config_filename=config_file, fees=fees, inputs=num_inputs)
	else:
		net = Bot(fees=fees, inputs=num_inputs)
	data_entry = 0
	for single_data in data:
		all_data = single_data.split("\n")
		times = []
		prices = []
		for data_slice in all_data:
			if data_slice != "":
				slice_pieces = data_slice.split(",")
				time = float(slice_pieces[0])
				price = float(slice_pieces[1])
				times[:0] = [time]
				prices[:0] = [price]
				times = times[:max_d]
				prices = prices[:max_d]
				if len(times) == max_d:
					data = []
					approx_prices = []
					approx_times = []
					i = 0
					while i < len(prices):
						approx_prices.append(avg(prices[i:min(i+approx,len(prices))]))
						approx_times.append(avg(times[i:min(i+approx,len(times))]))
						i+=approx
					sz = math.floor(len(approx_prices)/2.0)
					data.append(calc_slope(approx_times[:sz], approx_prices[:sz]))
					data.append(calc_curl(approx_times[:sz], approx_prices[:sz]))
					data.append(calc_slope(approx_times, approx_prices))
					data.append(calc_curl(approx_times, approx_prices))
					data.append((prices[0]-approx_prices[0])/prices[0])
					net.feed_data(data)
					net.propagate()
					output = net.determine_output()
					if output == 0:
						if (money/float(prices[0]) > minimum_crypto):
							crypto_delta = round((money*.98)/prices[0],8)
							crypto_wallet += crypto_delta
							money -= calc_dues(float(crypto_delta)*prices[0], net.fees, True)
							hit = [(86400.00*data_entry)+time,price]
							buys.append(hit)
					elif output == 2:
						if (crypto_wallet > minimum_crypto):
							crypto_delta = crypto_wallet
							crypto_wallet = 0
							hit = [(86400.00*data_entry)+time,price]
							money += calc_dues(float(crypto_delta)*prices[0], net.fees, False)
							sells.append(hit)
		data_entry += 1
	crypto_delta = crypto_wallet
	crypto_wallet = 0
	money += (float(crypto_delta)*prices[0])
	return money, net


b_train = ["131.csv","132.csv","133.csv","134.csv","135.csv", "136.csv", "137.csv", "138.csv", "139.csv", "140.csv", "141.csv", "142.csv", "143.csv", 
"144.csv", "145.csv", "146.csv", "147.csv", "148.csv", "149.csv", "150.csv", 
"151.csv", "152.csv", "153.csv", "154.csv", "155.csv"]
b_tests = ["156.csv", "157.csv", "158.csv", "159.csv", "160.csv", "161.csv"]
b_all = ["131.csv","132.csv","133.csv","134.csv","135.csv", "136.csv", 
"137.csv", "138.csv", "139.csv", "140.csv", "141.csv", "142.csv", "143.csv", 
"144.csv", "145.csv", "146.csv", "147.csv", "148.csv", "149.csv", "150.csv", 
"151.csv", "152.csv", "153.csv", "154.csv", "155.csv", "156.csv", "157.csv",
"158.csv", "159.csv", "160.csv", "161.csv"]


if __name__ == '__main__':
	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()
	size = comm.Get_size()
	config_save = "bit_4py0.conf"
	val, bot = mpi_train(rank, size, b_train, 10000, 25, "bitcoin", .0001, fees=.0026)
	if rank == 0:
		bot.write_config(config_save)
