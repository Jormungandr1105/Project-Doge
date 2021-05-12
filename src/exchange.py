import shrimpy
import json


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
		print("#"*80)
		print("# EXCHANGE INFORMATION #"+"#"*56)
		print("#"*80)
		print("# USERNAME: "+self.username)
		print("# USER_ID: "+self.user_id)
		print("#"+" "*78+"#")
		print("# DEFAULT_EXCHANGE_NAME: "+str(self.default_account_name))
		print("# DEFAULT_EXCHANGE_ID: "+str(self.default_account_id)+"\n#")
		#for set in self.default_trading_pairs:
			#print("# "+set["baseTradingSymbol"]+" --> "+set["quoteTradingSymbol"])
		print("# EXCHANGES: "+" "*66+"#\n"+"#"*80)
		for account in self.accounts:
			print("# EXCHANGE_NAME: "+account["exchange"])
			print("# EXCHANGE_ID: "+str(account["id"]))
			balance = self.get_balance(account["id"])
			for crypto in balance:
				print("## "+str(crypto)+": "+str(balance[crypto]))
			print("#"*80)

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
		#print(trade_response)
		print(trade_response["id"])
		self.current_trades.append(trade_response["id"])

	def check_trades(self):
		# Check in on ongoing trades, chnage balances when completed
		for trade in self.current_trades:
			response = self.client.get_trade_status(self.user_id,self.default_account_id, trade)
			if (response["trade"]["status"] == "completed" and response["trade"]["success"] == True):
				for change in response["changes"]:
					if change["symbol"] in self.default_balances:
						self.default_balances[change["symbol"]] = self.default_balances[change["symbol"]] + float(change["nativeValue"])
					else:
						self.default_balances[change["symbol"]] = float(change["nativeValue"])
				self.current_trades.remove(trade)
			elif (response["trade"]["status"] == "completed" and response["trade"]["success"] == False):
				print("Trade Failed")
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