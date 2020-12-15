import guiscreen;
import overlay;
import pygame;

KEYBIND_GUI = {
	pygame.K_ESCAPE : "GamePaused"
};

class GamePaused(guiscreen.GUI):
	def __init__(self, main):
		super().__init__("Game Paused", "GamePaused", "When game is paused.");

		self.main = main;

	def closed(self):
		self.main.camera_manager.focused = True;
	
		overlay.SPLIT = 1;

	def opened(self):
		overlay.SPLIT = 0;

		self.main.camera_manager.focused = False;

	def on_click_up(self, button):
		if button == 1:
			self.close();

	def on_render(self):
		self.main.font_renderer.draw("Game Paused", 10, 10, [255, 0, 255]);
