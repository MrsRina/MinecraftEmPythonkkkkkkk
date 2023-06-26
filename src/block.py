from OpenGL import GL as GL11;
from api    import util;

import pygame;
import os;

# Mapeamos aqui as faces e suas respectivas sequencias.
FACES = ["back", "down", "front", "left", "right", "up"];

class Face:
	def __init__(self, name):
		self.name = name;
		self.face = util.Vec(0, 0, 0);

# eu sou transexual, eu irei me assumir, se voce esta lendo saiba que eu sou.
# - Rina.
class Block:
	def __init__(self, name, current_path_textures = None):
		self.name = name;
		self.aabb = util.AABB();

		self.position = util.Vec(0.0, 0.0, 0.0);

		# blocos na teoria tem yaw e pitch simmm.
		self.yaw   = 0;
		self.pitch = 0;

		self.aabb.max.x = 1;
		self.aabb.max.y = 1;
		self.aabb.max.z = 1;

		self.textures = {};
		self.faces    = {};

		self.render_list = GL11.glGenLists(1);

		self.transparency = False;
		self.alpha        = 255;

		if None != current_path_textures:
			for faces in FACES:
				face = Face(faces);

				self.faces[faces] = face;

				path = os.path.join(os.path.abspath(current_path_textures + name + "_" + faces));

				self.textures[faces] = util.convert_to_texture(pygame.image.load(path + ".png"));

		GL11.glNewList(self.render_list, GL11.GL_COMPILE);
		GL11.glColor(1, 1, 1);

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["front"]);

		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["back"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0)
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["left"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["right"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["up"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["down"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
		GL11.glDisable(GL11.GL_TEXTURE_2D);

		GL11.glEndList();

	def on_render(self):
		self.aabb.min.x = -self.position.x;
		self.aabb.min.y = -self.position.y;
		self.aabb.min.z = -self.position.z;

		# aqui eu desenho a pora, o que e pora;
		GL11.glPushMatrix();
		GL11.glTranslate(-self.position.x, -self.position.y, -self.position.z);

		if self.transparency:
			GL11.glEnable(GL11.GL_BLEND);
			GL11.glBlendFunc(GL11.GL_SRC_ALPHA, GL11.GL_ONE_MINUS_SRC_ALPHA);

			GL11.glColor(1, 1, 1, self.alpha / 255.0);

		GL11.glColor(1, 1, 1);

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["front"]);

		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["back"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0)
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["left"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["right"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["up"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y + self.aabb.max.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["down"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.aabb.min.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z + self.aabb.max.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.aabb.min.x + self.aabb.max.x, self.aabb.min.y, self.aabb.min.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
		GL11.glDisable(GL11.GL_TEXTURE_2D);

		if self.transparency:
			GL11.glDisable(GL11.GL_BLEND);

		GL11.glPopMatrix();