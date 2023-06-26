from api import util;

from OpenGL import GL as GL11;

import pygame;
import os;

import block;

# filho de um anao
class Skybox:
	x = 0;
	y = 0;
	z = 0;

	w = 4096;
	h = 4096;
	l = 4096;

	def __init__(self, path):
		self.textures = {};

		for sides in block.FACES:
			file_path = os.path.join(os.path.abspath(path + sides));

			self.textures[sides] = util.convert_to_texture(pygame.image.load(file_path + ".png"));

		self.list = GL11.glGenLists(1);

		self.x = self.x - self.w / 2;
		self.y = self.y - self.h / 2;
		self.z = self.z - self.l / 2;

	def prepare(self):
		GL11.glNewList(self.list, GL11.GL_COMPILE);
		GL11.glColor(1, 1, 1);

		GL11.glEnable(GL11.GL_TEXTURE_2D);
		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["front"]);

		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x + self.w, self.y, self.z + self.l);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["back"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 0)
		GL11.glVertex3f(self.x + self.w, self.y, self.z);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x, self.y, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["left"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x, self.y, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["right"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x + self.w, self.y, self.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x + self.w, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["up"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x + self.w, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x, self.y + self.h, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, self.textures["down"]);
		GL11.glBegin(GL11.GL_QUADS);
		GL11.glTexCoord2f(0, 0);
		GL11.glVertex3f(self.x, self.y, self.z);
		GL11.glTexCoord2f(1, 0);
		GL11.glVertex3f(self.x, self.y, self.z + self.l);
		GL11.glTexCoord2f(1, 1);
		GL11.glVertex3f(self.x + self.w, self.y, self.z + self.l);
		GL11.glTexCoord2f(0, 1);
		GL11.glVertex3f(self.x + self.w, self.y, self.z);
		GL11.glEnd();

		GL11.glBindTexture(GL11.GL_TEXTURE_2D, 0);
		GL11.glDisable(GL11.GL_TEXTURE_2D);

		GL11.glEndList();

	def on_render(self):
		GL11.glPushMatrix();
		GL11.glColor(1, 1, 1);
		GL11.glCallList(self.list);
		GL11.glColor(1, 1, 1);
		GL11.glPopMatrix();