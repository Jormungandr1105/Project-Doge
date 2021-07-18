class Node():

	def __init__(self, bias, prev_weights = None, value = None):
		self.bias = float(bias)
		if prev_weights is None:
			self.weights = []
		else:
			self.weights = []
			for x in prev_weights:
				self.weights.append(float(x))
		if value is None:
			self.value = 0.0
		else:
			self.value = float(value)

	
	# GETTERS
	def get_bias(self):
		return self.bias

	def get_value(self):
		return self.value

	def get_weight(self, x):
		return self.weights[x]

	def get_weights(self):
		return self.weights
	
	# SETTERS
	def set_value(self, value):
		self.value = value

	def set_weights(self, weights):
		self.weights = weights

	def set_weight(self, index, value):
		self.weights[index] = value

	def set_bias(self, bias):
		self.bias = bias