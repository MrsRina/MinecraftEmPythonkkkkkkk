#
# Created by Rina at 28/11/2020 at 11:32pm
#
# Main class and game client initializer.
#

from OpenGL import GL as GL11, GLU;

import pygame;
import time;

from api import util;

# Todos as fields daqui.
import camera;
import overlay;
import guiscreen;
import block;
import skybox;
import entity_manager;
import entity;
import os; 
from os import path;

import keyboard;
import game_gui;
import game_settings;
import world;

NAME    = "MinecraftkkkEmPython pora para de muda"
VERSION = "0.0.2";

SHOW_VERSION = True;
START        = True;

# oi oio  como eu vendo pessoas no python
class Main:
	screen_width  = 800;
	screen_height = 600;

	def __init__(self):
		pygame.init();

		self.refresh_size();

		pygame.display.set_caption(NAME + " " + (VERSION if SHOW_VERSION is True else ""));

	def set_new_title(self, title):
		pygame.display.set_caption(title + " - " + NAME + " " + (VERSION if SHOW_VERSION is True else ""));

	def refresh_size(self):
		flags = pygame.OPENGL | pygame.DOUBLEBUF; 

		if game_settings.CONFIG_FULLSCREEN:
			flags |= pygame.FULLSCREEN;

			self.screen_width  = game_settings.CONFIG_FULLSCREEN_RESOLUTION[0][0];
			self.screen_height = game_settings.CONFIG_FULLSCREEN_RESOLUTION[0][1];

		self.display = pygame.display.set_mode((self.screen_width, self.screen_height), flags);

	def set_size(self, w, h):
		self.screen_width  = w;
		self.screen_height = h;

		# Refrescar agua.
		self.refresh_size();

	def do_run(self):
		self.fov = game_settings.CONFIG_FOV; self.fog = 5000.0;

		self.camera_manager   = camera.CameraManager(self);
		self.overlay_manager  = overlay.OverlayManager(CURRENT_OPENGL = GL11, main = self);
		self.gui_manager      = guiscreen.GUIManager(self);
		self.keyboard_manager = keyboard.KeyBindingManager();

		self.clock = pygame.time.Clock();
		self.fps   = 240; # locked;

		self.clock.tick(self.fps);

		# Algumas coisas como peixes e negros.
		self.font_renderer          = util.CustomTextRender("Verdana", 19);
		self.last_delta_time        = 0;
		self.camera_manager.focused = True;
		self.entity_manager_        = entity_manager.EntityManager(self);
		overlay.SPLIT               = 1;
		self.background             = [190, 190, 190];

		# O skybox ou seja aquele bagulho do ceu, incesto insano
		self.skybox = skybox.Skybox("textures/skybox/");
		self.skybox.prepare();

		self.gui_manager.add(game_gui.GamePaused(self));
		self.gui_manager.add(game_gui.MainMenu(self));
		self.gui_manager.add(game_gui.Inventory(self));

		self.cancel_render_3D = False;

		self.world = world.World(self);
		self.world.load_chunk(1, 1);

		# Tem que cria o player.
		self.player = entity.EntityPlayer("Player", "Player", "Ngga");
		self.player.init();
		self.player.set_camera(True);
		self.player.fly = True;
		self.player.registry(420);

		self.world.implement_entity(self.player);

		# Tem que inisia, eu posso fazer um sistema de salvar keybinds,
		# mas isso nao vai ser taooo nesssesario agora, entao fica assim!
		self.init_keys();

		# Ok ele foi ativado entao.
		# Mas olha, eu fiz no final por que eu preciso iniciar 
		# antes as variaveis como 
		# cancel_render_3d
		# por que se nao da errokkk
		# ou seja, eu preciso cancelar o render 3D
		# depois que a variavel foi criada.
		self.gui_manager.open_gui("MainMenu");

		# Iniciamos o OpenGL e os estados e projecoes da matrix.
		GL11.glClearDepth(1)

		GL11.glViewport(0, 0, self.screen_width, self.screen_height);
		GL11.glMatrixMode(GL11.GL_PROJECTION);
		GL11.glLoadIdentity();
	
		GLU.gluPerspective(self.fov, (self.screen_width / self.screen_height), 0.1, self.fog);
	
		GL11.glMatrixMode(GL11.GL_MODELVIEW);
		GL11.glLoadIdentity();

		GL11.glDisable(GL11.GL_CULL_FACE);
		GL11.glEnable(GL11.GL_DEPTH_TEST);

		while (True):
			self.partial_ticks   = self.clock.tick(self.fps) / 60;
			self.delta_time      = self.partial_ticks - self.last_delta_time;
			self.last_delta_time = self.partial_ticks;

			GL11.glClear(GL11.GL_COLOR_BUFFER_BIT | GL11.GL_DEPTH_BUFFER_BIT);
			GL11.glClearColor(float(self.background[0] / 255.0), float(self.background[1] / 255.0), float(self.background[2] / 255.0), 1.0);

			GL11.glEnable(GL11.GL_DEPTH_TEST);

			if self.cancel_render_3D != True:
				self.render_3D();

			GL11.glPushMatrix();

			GL11.glViewport(0, 0, self.screen_width, self.screen_height);
			GL11.glMatrixMode(GL11.GL_PROJECTION);
			GL11.glLoadIdentity();
	
			GLU.gluOrtho2D(0, self.screen_width, self.screen_height, 0)
	
			GL11.glMatrixMode(GL11.GL_MODELVIEW);
			GL11.glLoadIdentity();

			GL11.glEnable(GL11.GL_CULL_FACE);
			GL11.glDisable(GL11.GL_DEPTH_TEST);

			self.render_2D();

			GL11.glDisable(GL11.GL_CULL_FACE);
			GL11.glEnable(GL11.GL_DEPTH_TEST);

			GL11.glViewport(0, 0, self.screen_width, self.screen_height);
			GL11.glMatrixMode(GL11.GL_PROJECTION);
			GL11.glLoadIdentity();
	
			GLU.gluPerspective(self.fov, (self.screen_width / self.screen_height), 0.1, self.fog);
	
			GL11.glMatrixMode(GL11.GL_MODELVIEW);
			GL11.glLoadIdentity();

			# vai se fuderkkkkk
			GL11.glPopMatrix();

			self.update_event();

			pygame.display.flip();

	def init_keys(self):
		# menstruasao do tevlado
		self.keyboard_manager.add("MoveForward", pygame.K_w);
		self.keyboard_manager.add("MoveBackward", pygame.K_s);
		self.keyboard_manager.add("MoveStrafeLeft", pygame.K_a);
		self.keyboard_manager.add("MoveStrafeRight", pygame.K_d);
		self.keyboard_manager.add("MoveJump", pygame.K_SPACE);
		self.keyboard_manager.add("MoveCrouch", pygame.K_LSHIFT);
		self.keyboard_manager.add("MoveSpriting", pygame.K_w); # duas vezesw veq

	def update_event(self):
		for current_event in pygame.event.get():
			if (current_event.type == pygame.QUIT):
				pygame.quit();

				# por que pedro perry.
				quit(); # por que voce quit
				# ele quitou...,

			if current_event.type == pygame.MOUSEBUTTONUP:
				self.gui_manager.update_click_up(current_event.button);

			if current_event.type == pygame.MOUSEBUTTONDOWN:
				self.gui_manager.update_click_down(current_event.button);

			self.entity_manager_.on_update_event(current_event);

		keys = pygame.key.get_pressed();

		# So pra ajudar a volta no 0, 0, 0 caso cair no fundo do mapa ou etc.
		if keys[pygame.K_r]:
			# sim eu sei que esta com a camera, mas vai!
			if self.player.camera():
				# nao e estatica, mas tem como k
				self.camera_manager.set_pos(1, 1, 1);

				# Meu amigro negro
				self.player.velocity = 0;

		self.entity_manager_.on_update();
		self.camera_manager.update_camera();
		self.entity_manager_.on_world_update(self.world);

		if self.gui_manager.current_gui != None:
			self.gui_manager.update_event_key(keys);

		if self.gui_manager.current_gui != self.gui_manager.get("GamePaused"):
			self.process_in_game_keys(keys);

	def process_in_game_keys(self, keys):
		if keys[pygame.K_ESCAPE] and self.gui_manager.current_gui == None:
			self.gui_manager.open_gui("GamePaused");

	def render_3D(self):
		# Fovdase?
		self.entity_manager_.on_render();
		self.camera_manager.render_split();
		self.world.update_render_3d();

		# ok liguei a lista criada na classe skybox que renderiza tudo.
		self.skybox.on_render();

	def render_2D(self):
		self.gui_manager.update_render();
		self.overlay_manager.on_render();

if (__name__ == "__main__"):
	game = Main();
	game.do_run();