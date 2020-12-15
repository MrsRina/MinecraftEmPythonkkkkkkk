# Aqui e tudo da overlay, render stack, posicao, 
# na real aqui e a render de tudo ou seja, eu irei ativar as coisas na main
# e vao ser renderizadas aqui, e um sistema de instancias;

SPLIT       = 0; # 0 false 1 true;
SPLIT_COLOR = [255, 0, 255];
SPLIT_SIZE  = 4; # Tamanho da bolakk

class OverlayManager:
	def __init__(self, CURRENT_OPENGL, main):
		self.GL11 = CURRENT_OPENGL;
		self.main = main;

	def on_render(self):
		# So por que nao quero botar self em tudo, mas que seja e python.
		GL11 = self.GL11;
		main = self.main;

		if (SPLIT):
			GL11.glPushMatrix();

			GL11.glEnable(GL11.GL_POINT_SMOOTH);
			GL11.glPointSize(SPLIT_SIZE);

			GL11.glColor(SPLIT_COLOR[0] / 255.0, SPLIT_COLOR[1] / 255.0, SPLIT_COLOR[2] / 255.0);

			GL11.glBegin(GL11.GL_POINTS);
			GL11.glVertex(main.screen_width / 2, main.screen_height / 2);
			GL11.glEnd();

			GL11.glDisable(GL11.GL_POINT_SMOOTH);

			GL11.glPopMatrix();