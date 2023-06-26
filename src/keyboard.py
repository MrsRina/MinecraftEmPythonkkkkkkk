import pygame;

class KeyBindingManager:
	def __init__(self):
		self.key_bind_list = {};

	def add(self, name, key):
		self.key_bind_list[name] = key;

	def remove(self, name):
		try:
			del self.key_bind_list[name];
		except:
			# so ignorakkk
			pass

	def get(self, name):
		return self.key_bind_list[name];

	def set(self, name, update_key):
		if (self.key_bind_list.__contains__(name)):
			self.key_bind_list[name] = update_key;

	def is_pressed(self, name):
		keys = pygame.key.get_pressed();

		return keys[self.key_bind_list[name]] == True;