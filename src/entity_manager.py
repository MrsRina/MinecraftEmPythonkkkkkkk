from api.util import lerp;
from math import pi;

import game_settings;

import pygame;

# oi
class EntityManager:
	def __init__(self, main):
		self.main = main;

		self.partial_ticks = 0.1;

	def on_update_event(self, current_event):
		for entities in self.main.world.loaded_entity_list:
			if entities.rendering:
				# Tiques parciais sao como um delta, nao muda nada.
				entities.update_event(self.main.camera_manager, self.main.keyboard_manager, current_event);

	def on_update(self):
		self.partial_ticks = self.main.partial_ticks / 0.1;

		for entities in self.main.world.loaded_entity_list:
			if entities.rendering:
				# Tiques parciais sao como um delta, nao muda nada.
				entities.update(self.main.camera_manager, self.main.keyboard_manager, 0.1);

	def on_world_update(self, the_world):
		for entities in the_world.loaded_entity_list:
			if entities.rendering:
				entities.world_update(the_world);

				if entities.get_health() <= 0:
					entities.set_living(False);

				if entities.is_spriting() and entities.camera() and not game_settings.CONFIG_STATIC_FOV:
					new_fov = (game_settings.CONFIG_FOV + ((entities.speed / 360) * pi) + (1.5 if entities.is_flying() == True else 0) if game_settings.DEV_FOV_BASED_ON_SPEED == True else game_settings.DEV_FOV)

					self.main.fov = lerp(self.main.fov, new_fov, self.main.partial_ticks);
				else:
					self.main.fov = lerp(self.main.fov, game_settings.CONFIG_FOV, self.main.partial_ticks);

	def on_render(self):
		for entities in self.main.world.loaded_entity_list:
			if entities.rendering:
				entities.render();