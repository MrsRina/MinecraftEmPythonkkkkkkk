import guiscreen;
import pygame;

KEYBIND_GUI = {
	pygame.K_ESCAPE : "GamePaused"
};

class GamePaused(guiscreen.GUI):
	def __init__(self, main):
		super().__init__("Game Paused", "GamePaused", "When game is paused.");

		self.main = main;

	def on_render(self):
		self.main.font_renderer.draw("Game Paused", 10, 10, [255, 0, 255]);
