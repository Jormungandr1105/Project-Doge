import shrimpy
import json


class Exchange():

	accounts = []
	current_trades = []
	default_account_id = 0
	default_account_name = "NULL"

	def __init__(self, shrimp_keys, user_data, default_exch=None):
		self.client = shrimpy.ShrimpyApiClient(shrimp_keys[0], shrimp_keys[1])
		self.username = user_data[0]
		self.user_id = user_data[1]
		self.set_accounts()
		if default_exch is not None:
			if len(self.accounts) > 0:
				account = self.accounts[0]
				self.default_account_id = account["id"]
				self.default_account_name = account["exchange"]
		else:
			for account in self.accounts:
				if (default_exch == account["exchange"]):
					self.default_account_id = account["id"]
					self.default_account_name = account["exchange"]

	def remove_user(self, user_id):
		self.client.remove_user(user_id)

	def link_account(self, exchange_name, exchange_keys):
		self.client.link_account(self.user_id, exchange_name, exchange_keys[0], exchange_keys[1])
		

	def set_accounts(self):
		self.accounts = self.client.list_accounts(self.user_id)

	def print_useful_info(self):
		print("#"*80)
		print("# EXCHANGE INFORMATION #"+"#"*56)
		print("#"*80)
		print("# USERNAME: "+self.username)
		print("# USER_ID: "+self.user_id)
		print("# DEFAULT_EXCHANGE_NAME: "+str(self.default_account_name))
		print("# DEFAULT_EXCHANGE_ID: "+str(self.default_account_id)+"\n#")
		print("# EXCHANGES: "+" "*66+"#\n"+"#"*80)
		for account in self.accounts:
			print("# EXCHANGE_NAME: "+account["exchange"])
			print("# EXCHANGE_ID: "+str(account["id"]))
			print("#"*80)

	def create_trade(self,from_symbol,to_symbol,amt,exchange_id):
		# AMT is amount of FROM_SYMBOL
		trade_response = self.client.create_trade(self.user_id,exchange_id,from_symbol,to_symbol,amt)
		self.current_trades.append(trade_response)

	def check_trades(self):
		changes = {'USD' : 0.0,
							 'DOGE': 0.0,
							 'BTC' : 0.0,
							 'ETH' : 0.0}
		# Check in on ongoing trades, chnage balances when completed
		for trade in self.current_trades:
			response = self.client.get_trade_status(self.user_id,self.default_account_id, trade)
			if (response["trade"]["status"] == "completed"):
				for change in response["changes"]:
					if change["symbol"] in changes:
						changes[change["symbol"]] = changes[change["symbol"]] + float(change["nativeValue"])
					else:
						changes[change["symbol"]] = float(change["nativeValue"])
				self.current_trades.remove(trade)
		return changes


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