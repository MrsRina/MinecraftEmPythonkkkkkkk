# Sei lakkk so fiz por que achei legal usar data como boolean.
class DataManager:
	current_data = {};

	def __init__(self, context):
		self.context = context;

	def add_data_value(self, the_data_name, data):
		self.current_data[the_data_name] = data;

	def set_value_data(self, the_data_name, new_data):
		if self.current_data.__contains__(the_data_name):
			self.current_data[the_data_name] = new_data;

	def refactor_data_value(self, the_data_name, the_new_data_name):
		data_requested = self.current_data[the_data_name];

		self.current_data[the_new_data_name] = data_requested

		del self.current_data[the_data_name];

	def get(self, the_data_name):
		return self.current_data[the_data_name];