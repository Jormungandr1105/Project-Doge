#!/usr/bin/python3
##################
import Bot
try:
	import plot
	plotting=True
except ModuleNotFoundError:
	plotting=False

def train(read_from_config, config_save, csv_files, num_instances, num_generations, coin, minimum_crypto, fees = None):
	value, test_bot = Bot.train(csv_files,num_instances,num_generations, coin, minimum_crypto, config_file=read_from_config, fees=fees)
	print(value)
	test_bot.write_config(config_save)
	test_bot.write_history("buys.csv","sells.csv")
	

def run(config, data_csvs, coin, minimum_crypto, fees = None):
	price_path = "../{0}_price_history/".format(coin)
	for x in range(len(data_csvs)):
		f = open(price_path+str(data_csvs[x]))
		data = f.read()
		data_container = []
		f.close()
		data_container.append(data)
		value, resulting_bot = Bot.run_sim(data_container, minimum_crypto, config_file=config, fees=fees)
		print("FILE: {0}, END_VALUE: {1}".format(data_csvs[x],value))


def check_values(config_file, data_csvs, coin, minimum_crypto, buys_csv, sells_csv, fees = None):
	price_path = "../{0}_price_history/".format(coin)
	data_holder = []
	for data_csv in data_csvs:
		f = open(price_path+data_csv)
		print(price_path+data_csv)
		data_holder.append(f.read())
		f.close()
	value, test_bot = Bot.run_sim(data_holder, minimum_crypto, config_file=config_file, fees=fees)
	test_bot.write_history(buys_csv, sells_csv)
	print(value)

	plot.plot_buy_sell(histories_ext+buys_csv,histories_ext+sells_csv,data_csvs,price_path)


def sanity_check(config_file, data_csvs, coin, minimum_crypto, fees):
	price_path = "../{0}_price_history/".format(coin)
	data_holder = []
	for data_csv in data_csvs:
		f = open(price_path+data_csv)
		print(price_path+data_csv)
		data_holder.append(f.read())
		f.close()
	value, test_bot = Bot.run_sim(data_holder, minimum_crypto,config_file=config_file, fees=fees)
	print(value)
	for x in range(10):
		n_val, test_bot = Bot.run_sim(data_holder, minimum_crypto, parent=test_bot, percent_d=0, fees=fees)
		print(n_val)


train_csvs = ["105.csv","106.csv","107.csv","108.csv","109.csv","110.csv"]
test_csvs = ["121.csv","122.csv","123.csv","124.csv","125.csv","126.csv","127.csv","128.csv","129.csv","130.csv"]
ether_csvs = ["123.csv","124.csv"]
basic_training = ["127.csv"]
kinda_stable = ["124.csv","125.csv","126.csv","127.csv"]
all_csvs = ["105.csv","106.csv","107.csv","108.csv","109.csv","110.csv","121.csv","122.csv","123.csv","124.csv","125.csv","126.csv","127.csv","128.csv","129.csv","130.csv"]
big_loss = ["128.csv","129.csv","130.csv"]
b_train = ["131.csv","132.csv","133.csv","134.csv"]
b_tests = ["135.csv"]
b_all = ["130.csv","131.csv","132.csv","133.csv","134.csv","135.csv","136.csv"]


histories_ext = "../histories/"


if __name__ == "__main__":
	####### RUN CONFIGS ##########################################################
	read_from_config=None
	write_to_config="bit_4py_3.conf"
	coin = "bitcoin"
	minimum_crypto = .0001
	fees = .0026
	## Training_Configs ##########################################################
	train_bot=False
	training_data=b_train
	base_config=read_from_config
	save_config=write_to_config
	num_instances = 100
	num_generations = 10
	## Sim_Configs ###############################################################
	run_sim=True
	sim_csv_files=b_all
	sim_config_file = write_to_config
	## Plotting_Configs ##########################################################
	plotting=plotting
	plot_data=b_all
	plot_config_file = write_to_config
	buys="buys.csv"
	sells="sells.csv"
	##############################################################################
	if train_bot:
		train(base_config, save_config, training_data, num_instances, num_generations, coin, minimum_crypto, fees=fees)
	if run_sim:
		run(sim_config_file, sim_csv_files, coin, minimum_crypto, fees=fees)
	if plotting:
		check_values(plot_config_file, plot_data, coin, minimum_crypto, buys, sells, fees=fees)

	#sanity_check(base_config, train_csvs, coin, minimum_crypto, fees)