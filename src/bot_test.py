#!/usr/bin/python3
##################
import Bot
import plot


def train(read_from_config, config_save, csv_files, num_instances, num_generations):
	value, test_bot = Bot.train(csv_files,num_instances,num_generations,read_from_config)
	print(value)
	test_bot.write_config(config_save)
	test_bot.write_history("buys.csv","sells.csv")
	

def check_values(config_file, data_csvs, buys_csv, sells_csv):
	data_holder = []
	for data_csv in data_csvs:
		f = open(price_path+data_csv)
		data_holder.append(f.read())
		f.close()
	value, test_bot = Bot.run_sim(data_holder, config_file=config_file)
	test_bot.write_history(buys_csv, sells_csv)
	print(value)

	plot.plot_buy_sell(histories_ext+buys_csv,histories_ext+sells_csv,data_csvs,price_path)


def run(config, data_csvs):
	for x in range(len(data_csvs)):
		f = open(price_path+str(data_csvs[x]))
		data = f.read()
		data_container = []
		f.close()
		data_container.append(data)
		value, resulting_bot = Bot.run_sim(data_container,config_file=config)
		print("FILE: {0}, END_VALUE: {1}".format(data_csvs[x],value))


train_csvs = ["105.csv","106.csv","107.csv","108.csv","109.csv","110.csv"]
test_csvs = ["121.csv","122.csv","123.csv","124.csv"]
ether_csvs = ["../ethereum_price_history/123.csv","../ethereum_price_history/124.csv"]

price_path = "../dogecoin_price_history/"
histories_ext = "../histories/"


if __name__ == "__main__":
	####### RUN CONFIGS ##########################################################
	read_from_config=None
	write_to_config="temp2.conf"
	## Training_Configs ##########################################################
	train_bot=False
	training_data=train_csvs
	base_config=read_from_config
	save_config=write_to_config
	num_instances = 1000
	num_generations = 5
	## Sim_Configs ###############################################################
	run_sim=True
	sim_csv_files=test_csvs
	sim_config_file = write_to_config
	## Plotting_Configs ##########################################################
	plotting=True
	plot_data=test_csvs
	plot_config_file = write_to_config
	buys="buys.csv"
	sells="sells.csv"
	##############################################################################
	if train_bot:
		train(read_from_config, write_to_config, training_data, num_instances, num_generations)
	if run_sim:
		run(sim_config_file, sim_csv_files)
	if plotting:
		check_values(plot_config_file, plot_data, buys, sells)