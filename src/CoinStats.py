from pycoingecko import CoinGeckoAPI
import time
import math
import csv
import sys
# My files
import plot

class CoinStats():

	def __init__(self, coin, last_price = None):
		if last_price is None:
			self.last_price = 0.0
		else:
			self.last_price = last_price
		self.coin = coin
		self.current_price = 0.0
		self.time_offset = -14400 # EST offset
		self.cg = CoinGeckoAPI()
		self.last_time = self.current_time()
		self.day_no = self.set_day()
	
	def get_price(self):
		doge_info = self.cg.get_price(ids=self.coin, vs_currencies='usd')
		return doge_info[self.coin]['usd']

	def check_price(self):
		try:
			self.current_price = self.get_price()
			if (self.current_price != self.last_price):
				if (self.current_time() < self.last_time): # if new day, rename file
					self.day_no = self.set_day()
				self.last_time = self.current_time()
				self.append_to_file()
				self.last_price = self.current_price
				return True
		except KeyboardInterrupt:
			sys.exit(0)
		except:
			pass
		return False

	def set_day(self):
		day_offset = 105-18733 # didn't feel like actually figuring it out offset for: days since Jan 1st 2021
		day_no = math.floor((time.time()+self.time_offset)/86400) + day_offset
		self.price_file = "../{}_price_history/".format(self.coin)+str(day_no)+".csv"
		return day_no

	def current_time(self):
		return ((time.time()+self.time_offset) % 86400)

	def append_to_file(self):
		f = open(self.price_file, "a")
		f.write(str(self.last_time)+","+str(self.current_price)+"\n")
		f.close()

	def plot_data(self, filename_csv):
		csv_file = open(filename_csv)
		csv_data = csv.reader(csv_file)
		x = []
		y = []
		for row in csv_data:
			x.append(float(row[0]))
			y.append(float(row[1]))
		plot.plotXvY(x, y)