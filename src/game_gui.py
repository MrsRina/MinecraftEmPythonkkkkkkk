import guiscreen;
import overlay;
import pygame;

from OpenGL import GL as GL11;

from api.util import lerp, Rect;

KEYBIND_GUI = {
	pygame.K_ESCAPE : "GamePaused",
	pygame.K_e : "Inventory"
};

class GamePaused(guiscreen.GUI):
	def __init__(self, main):
		super().__init__("Game Paused", "GamePaused", "When game is paused.");

		self.main = main;

	def closed(self):
		pygame.mouse.set_pos(self.main.screen_width / 2, self.main.screen_height / 2);

		self.main.camera_manager.focused = True;
	
		overlay.SPLIT     = 1;
		overlay.DEVELOPER = 1;

	def opened(self):
		overlay.SPLIT     = 0;
		overlay.DEVELOPER = 0;

		self.main.camera_manager.focused = False;

	def on_click_up(self, button):
		if button == 1:
			self.close();

	def on_render(self):
		text = "Game Paused";

		self.main.font_renderer.draw(text, self.main.screen_width / 2 - self.main.font_renderer.get_width(text) / 2, self.main.screen_height / 2, [0, 0, 0]);

class MainMenu(guiscreen.GUI):
	def __init__(self, main):
		super().__init__("Main Menu", "MainMenu", "Main menu");

		self.main = main;
		self.rect = Rect("Mani Menu Test");

		self.start = False;

	def closed(self):
		self.main.gui_manager.close_gui();

		pygame.mouse.set_pos(self.main.screen_width / 2, self.main.screen_height / 2);

		self.main.camera_manager.focused = True;
	
		overlay.SPLIT     = 1;
		overlay.DEVELOPER = 1;

		self.main.cancel_render_3D = False;

		GL11.glClear(GL11.GL_COLOR_BUFFER_BIT | GL11.GL_DEPTH_BUFFER_BIT);
		GL11.glClearColor(float(self.main.background[0] / 255.0), float(self.main.background[1] / 255.0), float(self.main.background[2] / 255.0), 1.0);

	def opened(self):
		overlay.SPLIT     = 0;
		overlay.DEVELOPER = 0;

		self.main.camera_manager.focused = False;
		self.main.cancel_render_3D       = True;

	def on_click_up(self, button):
		if button == 1:
			self.start = True;

	def on_render(self):
		text = "Main Menu";

		self.main.font_renderer.draw(text, self.main.screen_width / 2 - self.main.font_renderer.get_width(text) / 2, self.main.screen_height / 2, [0, 0, 0]);

		if self.start:
			self.main.background[0] = lerp(self.main.background[0], 0, self.main.partial_ticks);
			self.main.background[1] = lerp(self.main.background[1], 0, self.main.partial_ticks);
			self.main.background[2] = lerp(self.main.background[2], 0, self.main.partial_ticks);

			if self.main.background[0] <= 10:
				self.main.background[0] = 190;
				self.main.background[1] = 190;
				self.main.background[2] = 190;

				self.close();

				self.start = False;

class Inventory(guiscreen.GUI):
	def __init__(self, main):
		super().__init__("Inventory", "Inventory", "Inventory");

		self.main = main;

	def closed(self):
		pygame.mouse.set_pos(self.main.screen_width / 2, self.main.screen_height / 2);

		self.main.camera_manager.focused = True;
	
		overlay.SPLIT     = 1;
		overlay.DEVELOPER = 1;

	def opened(self):
		overlay.SPLIT     = 0;
		overlay.DEVELOPER = 0;

		self.main.camera_manager.focused = False;

	def on_click_up(self, button):
		if button == 1:
			self.close();
	
	def on_render(self):
		text = "Inventory";
		coordinates = "Your in";

		height = self.main.font_renderer.get_height();
		
		self.main.font_renderer.draw(text, self.main.screen_width / 2 - self.main.font_renderer.get_width(text) / 2, self.main.screen_height / 2, [0, 0, 0]);
		
		#self.main.font_renderer.draw(coordinates + str(int(self.main.camera_manager.position.x)) + " " + str(int(self.main.camera_manager.position.y)) + " " + str(int(self.main.camera_manager.position.z)), 10, [0, 0, 0]);