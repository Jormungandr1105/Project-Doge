#/usr/bin/python3
import plot
import time
import datetime
import math


class MultiBot():

	filename = "../log.txt"
	conv_cost = .0020
	max_d = 10

	def __init__(self, coins, loss = 0.0026, exchange = None):
		self.coins = coins
		self.money = 0.00
		self.loss = loss
		self.exchange = exchange
		# Keep using the same one for a while
		#f = open(self.filename, "w+")
		#f.write("")
		#f.close()

	def run_sim(self,prices,percentages):
		markup = 2*self.loss+.005
		current_prices = [0.0 for _ in range(len(prices))]
		self.current_percentages = [0.0 for _ in range(len(prices))]
		for x in range(len(percentages[0])-1):
			for i in range(len(percentages)):
				current_prices[i] = prices[i][x+1]
				self.current_percentages[i] = percentages[i][x]
			if x == 0: # First Pass
				print(self.get_worth(current_prices))
				self.log(current_prices)

			ordered_indexes = sort(self.current_percentages)
			changed = False
			j = 0
			while (self.current_percentages[ordered_indexes[j]] > self.current_percentages[ordered_indexes[len(self.current_percentages)-1]]+ markup):
				if (self.buy(ordered_indexes[j],ordered_indexes[len(percentages)-1], current_prices)):
					changed = True
				j += 1
			# Let me know
			if changed:
				self.log(current_prices)
		for coin in self.coins:
			print(coin)
		print(self.get_worth(current_prices))

	def run_real(self, CS_OBJ, coin_symbols):
		assert(self.exchange is not None)
		markup = 2*self.loss+.005
		check_val = 120
		current_check_val = 0
		prev_prices = CS_OBJ.get_prices()
		apiConnected = True
		while True:
			try:
				prices = CS_OBJ.get_prices()
				tallies = 0
				for i in range(len(prices)):
					if prices[i] != prev_prices[i]:
						tallies += 1
				if tallies >= 4:
					self.current_percentages = []
					for j in range(len(prices)):
						self.current_percentages.append(float(prices[j])/float(prev_prices[j]))
					ordered_indexes = sort(self.current_percentages)
					changed = False
					j = 0
					while (self.current_percentages[ordered_indexes[j]] > self.current_percentages[ordered_indexes[len(self.current_percentages)-1]]+ markup):
						if (self.buy_real(ordered_indexes[j],ordered_indexes[len(self.coins)-1], prices, coin_symbols)):
							changed = True
						j += 1
					# Let me know
					if changed:
						self.log_real(prices, coin_symbols, get_day())
					prev_prices = prices
				if not apiConnected:
					apiConnected = True
					screen_log("API_RECONNECTED")
			except UnboundLocalError:
				if apiConnected:
					apiConnected = False
					screen_log("API_LOST")
			time.sleep(10)
			if current_check_val >= check_val and apiConnected:
				self.exchange.get_balance()
				current_check_val = 0
			current_check_val += 1

	def buy(self, from_index, to_index, current_prices):
		worth = current_prices[from_index] * self.coins[from_index][1] 
		if worth > 5.00:
			self.coins[from_index][1] = 0
			self.coins[to_index][1] += (worth / current_prices[to_index]) * (1-self.loss)
			return True
		return False

	def buy_real(self, from_index, to_index, current_prices, symbols):
		if symbols[from_index] in self.exchange.default_balances:
			worth = current_prices[from_index] * self.exchange.default_balances[symbols[from_index]]
		else:
			worth = 0.0
		if worth > 5.00:
			text = "SOLD {0} for {1}".format(symbols[from_index], symbols[to_index])
			screen_log(text)
			self.exchange.create_trade(symbols[from_index], symbols[to_index], trunc_after_dec(self.exchange.default_balances[symbols[from_index]],7))
			wait_for_confirmation(self.exchange)
			self.exchange.get_balance()
			return True
		return False

	def get_worth(self, current_prices):
		sum = self.money
		for x in range(len(self.coins)):
			sum += self.coins[x][1] * current_prices[x] * (1-self.loss)
		return "Current Worth: ${}".format(sum)

	def get_worth_real(self, current_prices, coin_symbols):
		sum = self.money
		for x in range(len(self.coins)):
			if coin_symbols[x] in self.exchange.default_balances:
				sum += self.exchange.default_balances[coin_symbols[x]] * current_prices[x] * (1-self.loss)
		return "Current Worth: ${}".format(sum)

	def cash_out(self, current_prices, from_index):
		if current_prices[from_index] * self.coins[from_index][1] > 5.00:
			self.money += current_prices[from_index] * self.coins[from_index][1] * (1-self.conv_cost)
			self.coins[from_index][1] = 0.0
			return True
		return False

	def cash_in(self, current_prices, index):
		if self.money > 5.00:
			# Convert cash to crypto
			self.coins[index][1] += (self.money / current_prices[index]) * (1-self.conv_cost)
			self.money = 0.00
			return True
		return False

	def log(self, current_prices):
		text = "["
		for coin in self.coins:
			text += "{0}:{1},".format(coin[0], coin[1])
		text += "] CASH: ${0} {1}\n".format(self.money,self.get_worth(current_prices))
		f = open(self.filename, "a")
		f.write(text)
		f.close()

	def log_real(self, current_prices, coin_symbols, day_no):
		text = "["
		for coin in self.coins:
			text += "{0}:{1},".format(coin[0], coin[1])
		text += "] CASH: ${0} {1}\n".format(self.money,self.get_worth_real(current_prices, coin_symbols))
		filename = "../transactions/{}.txt".format(day_no)
		f = open(filename, "a")
		f.write(text)
		f.close()


def sort(prices):
	prices_index = []
	while (len(prices) > len(prices_index)):
		index_ = 0
		max_ = 0
		for x in range(len(prices)):
			if prices[x] > max_ and x not in prices_index:
				max_ = prices[x]
				index_ = x
		prices_index.append(index_)
	return prices_index


# More Helper Functions
def wait_for_confirmation(EXCHANGE):
	while not EXCHANGE.check_trades():
		time.sleep(6)


def trunc_after_dec(number, after_dec):
	str_num = str(number)
	dot_index = str_num.find(".")
	if dot_index == -1:
		return number
	else:
		max_index = min(dot_index+after_dec+1, len(str_num))
		str_num = str_num[:max_index]
		return float(str_num)

def screen_log(output):
	c_time = datetime.datetime.now() # Date and Time
	print("{0}: {1}".format(c_time, output))

def get_day():
	day_offset = 105-18733 # didn't feel like actually figuring it out offset for: days since Jan 1st 2021
	day_no = math.floor((time.time()+-14400)/86400) + 105-18733 # Logic Spelt out in CoinStats, filled in here for brevity
	return day_no