#
# Created by Rina at 28/11/2020 at 11:32pm
#
# Main class and game client initializer.
#

from api.libs import GL as GL11, pygame, GLU;
from api.util import Render, lerp, Vec, CustomTextRender, clamp;

import math;

import camera;
import overlay;
import guiscreen;

import game_gui;

NAME    = "Survival Craft Python Edition"
VERSION = "0.0.1";

SHOW_VERSION = True;
START        = True;

RENDER = Render("0.0.1");

MASK_BLOCK = [
	[0, 0, 0],
	[0, 0, -1],
	[-1, 0, -1],
	[-1, 0, 0],

	[0, 0, 0],
	[-1, 0, 0],
	[-1, -1, 0],
	[0, -1, 0],

	[0, 0, 0],
	[0, -1, 0],
	[0, -1, -1],
	[0, 0, -1],

	[-1, 0, 0],
	[-1, 0, -1],
	[-1, -1, -1],
	[-1, -1, 0],

	[0, 0, 0],
	[0, -1, -1],
	[-1, -1, -1],
	[-1, -1, 0],

	[0, 0, 0],
	[-1, 0, -1],
	[-1, -1, -1],
	[0, -1, -1]
]

def render_polgyn(x, y, z, vertex_list):
	GL11.glPushMatrix();

	GL11.glTranslate(x, y, z);

	GL11.glEnable(GL11.GL_BLEND);
	GL11.glBlendFunc(GL11.GL_SRC_ALPHA, 771)

	GL11.glBegin(GL11.GL_QUADS);

	for vertex in vertex_list:
		GL11.glVertex(vertex[0], vertex[1], vertex[2]);

	GL11.glEnd();

	GL11.glPopMatrix();

def color(r, g, b, a = 255):
	GL11.glColor(clamp(r, 0, 255) / 255, clamp(g, 0, 255) / 255, clamp(b, 0, 255) / 255, clamp(a, 0, 255) / 255);

class Main:
	screen_width  = 800;
	screen_height = 600;

	def __init__(self):
		pygame.init();

		self.display = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.OPENGL | pygame.DOUBLEBUF);

		pygame.display.set_caption(NAME + " " + (VERSION if SHOW_VERSION is True else ""));

	def set_new_title(self, title):
		pygame.display.set_caption(title + " - " + NAME + " " + (VERSION if SHOW_VERSION is True else ""));

	def refresh_size(self):
		self.display = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.OPENGL | pygame.DOUBLEBUF);

	def set_size(self, w, h):
		self.screen_width  = w;
		self.screen_height = h;

		# Resize and define new display.
		self.refresh_size();

	def do_run(self):
		self.fov = 60; self.fog = 500;

		self.GL11 = GL11;

		GL11.glViewport(0, 0, self.screen_width, self.screen_height);
		GL11.glMatrixMode(GL11.GL_PROJECTION);
		GL11.glLoadIdentity();

		GLU.gluPerspective(self.fov, (self.screen_width / self.screen_height), 0.1, self.fog);

		GL11.glMatrixMode(GL11.GL_MODELVIEW);
		GL11.glLoadIdentity();

		self.camera_manager  = camera.Camera(self, False);
		self.overlay_manager = overlay.OverlayManager(CURRENT_OPENGL = GL11, main = self);
		self.gui_manager     = guiscreen.GUIManager();

		self.clock = pygame.time.Clock();
		self.fps   = 60; # locked;

		self.font_renderer = CustomTextRender("Tahoma", 19);

		self.partial_ticks   = self.clock.tick() / self.fps;
		self.last_delta_time = self.partial_ticks;

		self.camera_manager.focused = True;

		self.gui_manager.add(game_gui.GamePaused(self));

		while (True):
			self.partial_ticks   = self.clock.tick() / self.fps;
			self.delta_time      = self.partial_ticks;
			self.last_delta_time = self.partial_ticks; 

			self.update_event();

			GL11.glClear(GL11.GL_COLOR_BUFFER_BIT | GL11.GL_DEPTH_BUFFER_BIT);
			GL11.glClearColor(0.5, 0.5, 0.5, 0.5);

			self.render_3D();

			GL11.glPushMatrix();

			GL11.glViewport(0, 0, self.screen_width, self.screen_height);
			GL11.glMatrixMode(GL11.GL_PROJECTION);
			GL11.glLoadIdentity();
	
			GLU.gluOrtho2D(0, self.screen_width, self.screen_height, 0)
	
			GL11.glMatrixMode(GL11.GL_MODELVIEW);
			GL11.glLoadIdentity();

			self.render_2D();

			GL11.glViewport(0, 0, self.screen_width, self.screen_height);
			GL11.glMatrixMode(GL11.GL_PROJECTION);
			GL11.glLoadIdentity();
	
			GLU.gluPerspective(self.fov, (self.screen_width / self.screen_height), 0.1, self.fog);
	
			GL11.glMatrixMode(GL11.GL_MODELVIEW);
			GL11.glLoadIdentity();
	
			GL11.glPopMatrix();

			pygame.display.flip();

	def update_event(self):
		for current_event in pygame.event.get():
			if (current_event.type == pygame.QUIT):
				pygame.quit();

				quit();

			if current_event.type == pygame.MOUSEBUTTONUP:
				self.gui_manager.update_click_up(current_event.button);

				self.camera_manager.on_click_up(current_event.button);

			if current_event.type == pygame.MOUSEBUTTONDOWN:
				self.gui_manager.update_click_down(current_event.button);

				self.camera_manager.on_click_down(current_event.button);

			if current_event.type == pygame.KEYDOWN:
				try:
					self.gui_manager.get(game_gui.KEYBIND_GUI[current_event.key]).toggle();
				except:
					pass

		keys = pygame.key.get_pressed();

	def render_3D(self):
		color(255, 255, 255);
		render_polgyn(0, 0, -10, MASK_BLOCK);

		self.camera_manager.update_camera(0.1, self.screen_width, self.screen_height);

	def render_2D(self):
		self.overlay_manager.on_render();
		self.gui_manager.update_render();

if (__name__ == "__main__"):
	game = Main();

	game.do_run();