from api.util import Vec, Tick, lerp, add_angle_length, AABB, clamp;
from api.data_manager import DataManager;

from math import sqrt, pi, sin, cos;

import OpenGL.GL as GL11;
import pygame;

import block;

class Entity:
	def __init__(self, name, tag, description):
		self.name, self.tag, self.description = name, tag, description;

		self.flag = DataManager("Entity");

		self.position  = Vec(0, 0, 0);
		self.rendering = True;
		self.id = 0;

	def registry(self, id):
		self.id = id;

	def init(self):
		pass

	def update_event(self, camera_manager, keyboard_manager, event):
		if (self.rendering):
			pass

	def update(self, camera_manager, keyboard_manager, delta_time):
		if (self.rendering):
			pass

	def world_update(self):
		if (self.rendering):
			pass;

	def render(self):
		if (self.rendering):
			pass

	def get_rotation_vec(self, yaw, pitch):
		x = cos(-yaw * 0.017453292 - 3.1415927);
		y = sin(-yaw * 0.017453292 - 3.1415927);
		z = -cos(-pitch * 0.017453292);
		w = sin(-pitch * 0.017453292);

		return Vec((y * z), w, (x * z));

class EntityPlayer(Entity):
	wait_for_double_jump    = Tick();
	wait_for_double_forward = Tick();
	wait_for_delta_time     = Tick();

	def __init__(self, name, tag, description):
		super().__init__(name, tag, description);

		self.collide = True;
		self.physhic = True;
		self.fly     = True;

		# Dimensoes do peixe.
		self.width  = 0.3;
		self.height = 1;

		# Massa e delta time,
		self.delta_time = 0;
		self.ampl       = 0.999;

		# Basicamente e a rotacao da cabesa da entidade.
		self.yaw   = 0;
		self.pitch = 0;

		self.angle    = 0;
		self.velocity = 0;

		# Seria a distancia maxima pra captar algo no world.
		self.reach_distance = 5;
		self.raytrace = Vec(0, 0, 0);
		self.look_vec = Vec(0, 0, 0);

		# As variaveis basicas de movemento e acelelracao da entidade.
		self.speed_forward  = 300;
		self.speed_backward = 200;
		self.speed_strafe   = 250;
		self.speed_fly      = 250;

		self.speed = 0;

	def init(self):
		self.flag.add_data_value("Camera", False);
		self.flag.add_data_value("OnGround", False);
		self.flag.add_data_value("Living", True);
		self.flag.add_data_value("Walking", False);
		self.flag.add_data_value("Flying", False);
		self.flag.add_data_value("Health", 20); # Assim, a vida e 20 fovdasekk.
		self.flag.add_data_value("Spriting", False);

	def set_camera(self, boolean):
		self.flag.set_value_data("Camera", boolean);

	def camera(self):
		return self.flag.get("Camera");

	def set_on_ground(self, boolean):
		if (self.flag.get("Living") or self.flag.get("Health") > 0):
			self.flag.set_value_data("OnGround", boolean);

	def get_on_ground(self):
		return self.flag.get("OnGround");

	def set_living(self, boolean):
		if boolean:
			self.flag.set_value_data("Living", True);
			self.flag.set_value_data("Health", 20);

			self.rendering = True;
		else:
			self.flag.set_value_data("Living", False);
			self.flag.set_value_data("Health", 0);

			self.rendering = False;

	def is_living(self):
		return self.flag.get("Living");

	def set_walking(self, boolean):
		if ((self.flag.get("Living") or self.flag.get("Health") > 0) and self.flag.get("OnGround")):
			self.flag.set_value_data("Walking", boolean);

	def is_walking(self):
		return self.flag.get("Walking");

	def set_flying(self, boolean):
		if (self.flag.get("Living") or self.flag.get("Health") > 0):
			self.flag.set_value_data("Flying", boolean);

	def is_flying(self):
		return self.flag.get("Flying");

	def set_health(self, number):
		if (self.flag.get("Living")):
			self.flag.set_value_data("Health", number);
		else:
			self.flag.set_value_data("Health", number);
			self.flag.set_value_data("Living", True);

			self.rendering = True;

	def get_health(self):
		return self.flag.get("Health");

	def set_spriting(self, boolean):
		if ((self.flag.get("Living") or self.flag.get("Health") > 0) and self.flag.get("OnGround")):
			self.flag.set_value_data("Spriting", boolean);

	def is_spriting(self):
		return self.flag.get("Spriting");

	def get_distance_from_block(self, block):
		x = ((block.position.x + block.aabb.max.x) - self.position.x);
		y = ((block.position.y + block.aabb.max.y) - (self.position.y - self.height));
		z = ((block.position.z + block.aabb.max.z) - self.position.z);

		return sqrt(x * x + y * y + z * z);

	def raytrace_block(self, block):
		reach = clamp(self.get_distance_from_block(block), 0, self.reach_distance);
		raytrace_ = Vec(self.position.x + (self.look_vec.x * reach), (self.position.y - self.height) + (self.look_vec.y * reach), self.position.z + (self.look_vec.z * reach));

		#print(reach, raytrace_.get());

		return raytrace_;

	def update_event(self, camera_manager, keyboard_manager, event):
		if self.rendering:
			# Nao pode ficar toda hora ligado se for pressionar, se nao ele vai dar uns problemas
			# de loop.
			if event.type == pygame.KEYDOWN:
				# Tipo se a variavel fly ter ligada, pra nao ser diretamente estatico,
				# meio que nao direto quando ativa o fly, eu posso simplismente
				# botar esse "evento" de se pressionar duas vezes o pular
				# ele vai pular, como no Minecraft, eu cho legalll.!!!
				# pra nao voar mais e so fazer denovo entao ele vai desligar!
				if event.key == keyboard_manager.get("MoveJump"):
					if not self.wait_for_double_jump.is_passed(500): # meio segundo.
						self.flag.set_value_data("Flying", not self.flag.get("Flying")); 

						# IMPORTANTE, ENGRO!
						# - seto x = !x;
						# ou seja, defino x como o contrario valor dele, caso x nao for igual 
						# a true, ele ira retornar a false, se ele for false, quer dizer que o 
						# comparador esta retornado a true pelo fato de ele nao ser igual a true
						# ta entendeu, isso se chama toggle, polo menos e o que eu chamo
						# 
						# boolean a = false;
						# a = !a; // como o not do self.flag.get("Flying");
						#
					else:
						self.wait_for_double_jump.reset();

				if event.key == keyboard_manager.get("MoveSpriting") and (self.flag.get("OnGround") or self.flag.get("Flying")):
					if not self.wait_for_double_forward.is_passed(500):
						self.flag.set_value_data("Spriting", True);
					else:
						self.wait_for_double_forward.reset();

	def update(self, camera_manager, keyboard_manager, delta_time):
		if self.rendering:
			if self.flag.get("Camera") and camera_manager.focused:
				self.yaw   = camera_manager.yaw;
				self.pitch = camera_manager.pitch;

				camera_manager.position = self.position;

				# Lupa sempre pra false, ai se eu ando ele muda corretamente.
				self.flag.set_value_data("Walking", False);

				if keyboard_manager.is_pressed("MoveForward"):
					self.position.x -= camera_manager.calcule_x_from_angle(self.yaw) * ((self.speed_forward / 1000) * 0.1);
					self.position.z -= camera_manager.calcule_z_from_angle(self.yaw) * ((self.speed_forward / 1000) * 0.1);

					self.flag.set_value_data("Walking", True);

				if keyboard_manager.is_pressed("MoveBackward"):
					self.position.x += camera_manager.calcule_x_from_angle(self.yaw) * ((self.speed_backward / 1000) * 0.1);
					self.position.z += camera_manager.calcule_z_from_angle(self.yaw) * ((self.speed_backward / 1000) * 0.1);

					self.flag.set_value_data("Walking", True);

				if keyboard_manager.is_pressed("MoveStrafeLeft"):
					self.position.x += camera_manager.calcule_x_from_angle(self.yaw - 90) * ((self.speed_strafe / 1000) * 0.1);
					self.position.z += camera_manager.calcule_z_from_angle(self.yaw - 90) * ((self.speed_strafe / 1000) * 0.1);

					self.flag.set_value_data("Walking", True);

				if keyboard_manager.is_pressed("MoveStrafeRight"):
					self.position.x -= camera_manager.calcule_x_from_angle(self.yaw - 90) * ((self.speed_strafe / 1000) * 0.1);
					self.position.z -= camera_manager.calcule_z_from_angle(self.yaw - 90) * ((self.speed_strafe / 1000) * 0.1);

					self.flag.set_value_data("Walking", True);

				# Ai eu crio o normal se for pressionado, ai ele so vai vua e tals.
				if keyboard_manager.is_pressed("MoveJump"):
					# Ainda uso o fly, pra ter 2 etapas, caso contrario alguem pode alterar
					# ok ninguem vai, mas pra ter uma ideia de flag 
					# em um jogo grande, aonde 2 ou mais variaveis pra habilitar algo faz a diferenca
					# voce nao pode voar se nao estar no criativo, se nao estiver com elytra...
					# mesma coisa aqui, ok voce pode so fazer mc.player.isFly = true;
					# mas isso nao e eficaz, quer dizer e..., mas em questoes de jogo!
					if self.fly and self.flag.get("Flying"):
						self.position.y += (self.speed_fly / 1000) * delta_time;

				if keyboard_manager.is_pressed("MoveCrouch"):
					if self.fly and self.flag.get("Flying"):
						self.position.y -= (self.speed_fly / 1000) * delta_time;

				# Se por acaso a bind do sprint for igual ao do andar pra frente
				# eu posso verificar se a bind do correr esta desligada caso 
				# estiver correndo, ai ele seta pra false.
				if keyboard_manager.is_pressed("MoveSpriting") == keyboard_manager.get("MoveForward"):
					if not keyboard_manager.is_pressed("MoveSpriting") and self.flag.get("Spriting"):
						self.flag.set_value_data("Spriting", False);
				else:
					# Aqui e a mesma coisa de cima, unico porem e que a bind de correr nao e igual ao
					# de andar.
					if not keyboard_manager.is_pressed("MoveForward") and self.flag.get("Spriting"):
						self.flag.set_value_data("Spriting", False);

				if self.flag.get("Spriting"):
					self.speed_forward  = lerp(self.speed_forward, 600, delta_time);
					self.speed_backward = lerp(self.speed_backward, 220, delta_time);
					self.speed_strafe   = lerp(self.speed_strafe, 300, delta_time);

					self.flag.set_value_data("Walking", True);
				else:
					# Seria a fisica.
					if self.flag.get("OnGround") or self.flag.get("Flying"):
						self.speed_forward  = lerp(self.speed_forward, 300, delta_time);
						self.speed_backward = lerp(self.speed_backward, 200, delta_time);
						self.speed_strafe   = lerp(self.speed_strafe, 250, delta_time);
					else:
						self.speed_forward  = lerp(self.speed_forward, 150, delta_time);
						self.speed_backward = lerp(self.speed_backward, 75, delta_time);
						self.speed_strafe   = lerp(self.speed_strafe, 100, delta_time);

	def world_update(self, the_world):
		if self.rendering:
			self.look_vec = self.get_rotation_vec(self.yaw, self.pitch);
			self.raytrace = Vec(self.position.x + (self.look_vec.x * self.reach_distance), self.position.y + (self.look_vec.y * self.reach_distance), self.position.z + (self.look_vec.z * self.reach_distance));

			print(self.raytrace.get());

			self.speed = sqrt(self.speed_forward * self.speed_forward + self.speed_backward + self.speed_strafe * self.speed_strafe);

			if not self.flag.get("OnGround") and not self.flag.get("Flying"):
				self.delta_time = self.wait_for_delta_time.current_ticks() / 100;
			else:
				self.wait_for_delta_time.reset();

				self.delta_time = 0;

			if self.physhic and not self.flag.get("Flying"):
				self.angle, self.velocity = add_angle_length(self.angle, self.velocity, pi, the_world.gravity);

				self.position.y += cos(self.angle) * self.velocity;

				self.velocity *= self.ampl;
			else:
				self.velocity = 0;

	def render(self):
		if (self.rendering):
			pass