import pygame;

# Preciso fazer um GUI manager seja, main menu, inventorio, ou que se foda.

class GUI:
	def __init__(self, name, tag, when):
		self.name = name; self.tag = tag; self.when = when;

		# Quando True vai renderizar a GUI, mas nao os estados dela.
		self.active = False;

	def open(self):
		if self.active == False:
			self.opened();

			self.active = True;

	def close(self):
		if self.active == True:
			self.closed();

			self.active = False;

	def toggle(self):
		if self.active:
			self.close();
		else:
			self.open();

	# Todos os overrides da GUI ou seja, quando desenharmos teremos que usar.
	def closed(self):
		override = True;

	def opened(self):
		override = True;

	def on_click_up(self, button):
		override = True;

	def on_click_down(self, button):
		override = True;

	def on_render(self):
		override = True;

class GUIManager:
	def __init__(self, main):
		self.list_gui    = [];
		self.current_gui = None;

		self.main = main;

	def add(self, gui):
		self.list_gui.append(gui);

	def get(self, gui):
		for guis in self.list_gui:
			if guis.tag == gui:
				return guis;

		return None;

	def toggle_gui(self, gui):
		_gui = self.get(gui);

		if (None != type(_gui)):
			self.current_gui = _gui;

			if self.current_gui.active == False:				
				self.current_gui.open();
			else:
				self.current_gui.close();

	def open_gui(self, gui):
		_gui = self.get(gui);

		if (None != type(_gui)):
			self.current_gui = _gui;

			if self.current_gui.active == False:
				self.current_gui.open();

	def close_gui(self):
		pygame.mouse.set_pos(self.main.screen_width / 2, self.main.screen_height / 2);

		self.current_gui = None;

	def update_click_up(self, button):
		if self.current_gui is not None:
			self.current_gui.on_click_up(button);

	def update_click_down(self, button):
		if self.current_gui is not None:
			self.current_gui.on_click_down(button);

	def update_event_key(self, keys):
		if self.current_gui is not None and keys[pygame.K_ESCAPE]:
			self.current_gui.close();

	def update_render(self):
		if self.current_gui is not None:
			self.current_gui.on_render();
