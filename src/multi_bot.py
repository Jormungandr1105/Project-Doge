#/usr/bin/python3
import plot

class MultiBot():

	filename = "../log.txt"
	conv_cost = .0020
	max_d = 10

	def __init__(self, coins, loss = 0.0026):
		self.coins = coins
		self.money = 0.00
		self.loss = loss
		f = open(self.filename, "w+")
		f.write("")
		f.close()

	def run_sim(self,prices,percentages,perc_avgs):
		markup = 2*self.loss+.005
		current_prices = [0.0 for _ in range(len(prices))]
		self.current_percentages = [0.0 for _ in range(len(prices))]
		self.avg_percs = []
		for x in range(len(percentages[0])-1):
			for i in range(len(percentages)):
				current_prices[i] = prices[i][x+1]
				self.current_percentages[i] = percentages[i][x]
				self.avg_percs[:0] = [perc_avgs[x]]
				self.avg_percs = self.avg_percs[:self.max_d]
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

	def buy(self, from_index, to_index, current_prices):
		worth = current_prices[from_index] * self.coins[from_index][1] 
		if worth > 5.00:
			self.coins[from_index][1] = 0
			self.coins[to_index][1] += (worth / current_prices[to_index]) * (1-self.loss)
			return True
		return False

	def get_worth(self, current_prices):
		sum = self.money
		for x in range(len(self.coins)):
			sum += self.coins[x][1] * current_prices[x] * (1-self.loss)
		return "Current Worth: ${}".format(sum)

	def cash_out(self, current_prices, from_index):
		if current_prices[from_index] * self.coins[from_index][1] > 5.00:
			self.money += current_prices[from_index] * self.coins[from_index][1] * (1-self.conv_cost)
			self.coins[from_index][1] = 0.0
			return True
		return False

	def cash_in(self, current_prices, index):
		if self.money > 5.00:
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
