# Preciso fazer um GUI manager seja, main menu, inventorio, ou que se foda.

class GUI:
	def __init__(self, name, tag, when):
		self.name = name; self.tag = tag; self.when = when;

		# Quando True vai renderizar a GUI, mas nao os estados dela.
		self.active = False;

	def open(self):
		self.active = True;

	def close(self):
		self.active = False;

	def toggle(self):
		self.active = self.active != True;

	# Todos os overrides da GUI ou seja, quando desenharmos teremos que usar.
	def on_click_up(self, button):
		override = True;

	def on_click_down(self, button):
		override = True;

	def on_render(self):
		override = True;

class GUIManager:
	def __init__(self):
		self.list_gui = [];

	def add(self, gui):
		self.list_gui.append(gui);

	def get(self, gui):
		for guis in self.list_gui:
			if guis.tag == gui:
				return guis;

		return None;

	def update_click_up(self, button):
		for guis in self.list_gui:
			if guis.active:
				guis.on_click_up(button);

	def update_click_down(self, button):
		for guis in self.list_gui:
			if guis.active:
				guis.on_click_down(button);

	def update_render(self):
		for guis in self.list_gui:
			if guis.active:
				guis.on_render();