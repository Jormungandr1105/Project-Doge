import shrimpy
import json
import time


title_card_file = "../jsons/title_block.txt"


class Exchange():

	accounts = []
	current_trades = []
	default_account_id = 0
	default_account_name = "NULL"
	default_trading_pairs = []
	default_balances = {}

	def __init__(self, shrimp_keys, user_data, default_exch=None):
		self.client = shrimpy.ShrimpyApiClient(shrimp_keys[0], shrimp_keys[1])
		self.username = user_data[0]
		self.user_id = user_data[1]
		self.set_accounts()
		if default_exch is None:
			if len(self.accounts) > 0:
				account = self.accounts[0]
				self.default_account_id = account["id"]
				self.default_account_name = account["exchange"]
		else:
			for account in self.accounts:
				if (default_exch == account["exchange"]):
					self.default_account_id = account["id"]
					self.default_account_name = account["exchange"]
		if self.default_account_name != "NULL":
			self.default_trading_pairs = self.client.get_trading_pairs(self.default_account_name)

	def remove_user(self, user_id):
		self.client.remove_user(user_id)

	def link_account(self, exchange_name, exchange_keys):
		self.client.link_account(self.user_id, exchange_name, exchange_keys[0], exchange_keys[1])
		self.set_accounts()
	
	def check_conversion(self,fromSymbol,toSymbol):
		for set in self.default_trading_pairs:
			if set["baseTradingSymbol"] == fromSymbol:
				if set["quoteTradingSymbol"] == toSymbol:
					return True
		return False

	def set_accounts(self):
		self.accounts = self.client.list_accounts(self.user_id)

	def print_useful_info(self):
		f = open(title_card_file,"r")
		title_text = f.read()
		title_data = title_text.split("\n")
		print("#"*80)
		time.sleep(.1)
		for x in title_data:
			self.print_bracketed(x)
			time.sleep(.2)
		time.sleep(.2)
		print("#"*80)
		time.sleep(.2)
		print("# EXCHANGE INFORMATION #"+"#"*56)
		time.sleep(.2)
		print("#"*80)
		time.sleep(.2)
		self.print_bracketed(" USERNAME: "+self.username)
		time.sleep(.2)
		self.print_bracketed(" USER_ID: "+self.user_id)
		time.sleep(.2)
		print("#"+" "*78+"#")
		time.sleep(.2)
		self.print_bracketed(" DEFAULT_EXCHANGE_NAME: "+str(self.default_account_name))
		time.sleep(.2)
		self.print_bracketed(" DEFAULT_EXCHANGE_ID: "+str(self.default_account_id))
		time.sleep(.2)
		print("#"+" "*78+"#")
		time.sleep(.2)
		print("# EXCHANGES: "+" "*66+"#\n"+"#"*80)
		time.sleep(.2)
		for account in self.accounts:
			self.print_bracketed(" EXCHANGE_NAME: "+account["exchange"])
			time.sleep(.2)
			self.print_bracketed(" EXCHANGE_ID: "+str(account["id"]))
			time.sleep(.2)
			balance = self.get_balance(account["id"])
			for crypto in balance:
				self.print_bracketed("# "+str(crypto)+": "+str(balance[crypto]))
				time.sleep(.1)
			print("#"*80)

	def print_bracketed(self, string):
		print("#"+string+"."*(78-len(string))+"#")

	def get_balance(self, account_id=None):
		current_balances  = {}
		if account_id is not None:
			acct_id = account_id
		else:
			acct_id = self.default_account_id
		balances = self.client.get_balance(self.user_id,acct_id)
		for balance in balances["balances"]:
			current_balances[balance["symbol"]] = balance["nativeValue"]
		if account_id is None:
			self.default_balances = current_balances
		return current_balances

	def save_balance(self, balance_file):
		f = open(balance_file,"w+")
		json.dump(self.default_balances,f,indent=2)
		f.close()

	def create_trade(self,from_symbol,to_symbol,amt):
		# AMT is amount of FROM_SYMBOL
		trade_response = self.client.create_trade(self.user_id,self.default_account_id,from_symbol,to_symbol,amt)
		try:
			print(trade_response["id"])
			self.current_trades.append(trade_response["id"])
		except KeyError:
			print('["id"] key error')
			print(trade_response)
			self.get_balance()

	def check_trades(self):
		# Check in on ongoing trades, change balances when completed
		for trade in self.current_trades:
			response = self.client.get_trade_status(self.user_id,self.default_account_id, trade)
			if (response["trade"]["status"] == "completed" and response["trade"]["success"] == True):
				self.get_balance()
				self.current_trades.remove(trade)
			elif (response["trade"]["status"] == "completed" and response["trade"]["success"] == False):
				print("Trade Failed")
				self.current_trades.remove(trade)
		return len(self.current_trades) == 0


def get_shrimpy_keys(filename):
	f = open(filename,"r")
	key_data = json.load(f)
	f.close()
	return (key_data["public_shrimpy"], key_data["private_shrimpy"])


def get_other_keys(filename, exchange_name):
	f = open(filename,"r")
	key_data = json.load(f)
	f.close()
	return (key_data["public_"+exchange_name], key_data["private_"+exchange_name])


def get_user_info(filename, user):
	f = open(filename,"r")
	data = json.load(f)
	f.close()
	user_data = data[user]
	return (user_data["username"], user_data["user_id"])