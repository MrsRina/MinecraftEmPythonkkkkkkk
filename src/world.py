from api import util;

import block;
import entity;

class World:
	def __init__(self, main):
		self.main               = main;
		self.loaded_entity_list = [];
		self.gravity            = 0.001;

		self.chunk = [];

	def load_chunk(self, size, length):
		# Limpamos a chunk atual.
		self.chunk.clear();

		# Aqui vamos criar uns bloquinhos e bem simples mesmo, so para testar chunk.
		for x in range(size):
			for z in range(size):
				_block = block.Block("dirty", "textures/blocks/");
				_block.position.x, _block.position.y, _block.position.z = x, length, z;

				self.chunk.append(_block);

	def get_entity_from_id(self, id):
		entity = None;

		for entities in self.loaded_entity_list:
			if entities.id == id:
				entity = entities;

				break;

		return entity;

	def implement_entity(self, _ent):
		if entity.EntityPlayer == type(_ent):
			self.loaded_entity_list.append(_ent);

	def kill_entity(self, _ent):
		if entity.EntityPlayer == type(_ent):
			self.get_entity(_ent.tag).set_living(False);

	def spawn_entity(self, _ent, position):
		# nao podemos spanawe algo vivido.
		if entity.EntityPlayer == type(_ent) and not _ent.is_living():
			self.get_entity(_ent.tag).set_living(True);

			# sim pernas de pau.
			self.get_entity(_ent.tag).position.x = position[0];
			self.get_entity(_ent.tag).position.y = position[1];
			self.get_entity(_ent.tag).position.z = position[2];

	def get_entity(self, entity_tag):
		for entities in self.loaded_entity_list:
			if entities.tag == entity_tag:
				return entities;

	def update_render_3d(self):
		for blocks in self.chunk:
			#print(self.main.player.get_block_aabb(blocks).get());

			if self.main.player.camera():
				raytrace_block = self.main.player.raytrace_block(blocks);

				# print(raytrace_block.get(), util.collide_aabb_vec(blocks.aabb, raytrace_block));

				if util.collide_aabb_vec(blocks.aabb, self.main.player.raytrace):
					blocks.transparency = True;
					blocks.alpha = 100;
				else:
					blocks.transparency = False;
					blocks.alpha = 255;

			blocks.on_render();