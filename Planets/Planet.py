from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np

class Planeta:
    def __init__(self, nombre, radio, texture, distancia_sol, dias_Sol):
        self.nombre = nombre
        self.radio = radio / 100
        self.segments = 30
        self.texture = f"./textura/{texture}.jpg"
        self.texture_id = self.load_texture()
        self.distancia_sol = distancia_sol
        self.dias_sol = dias_Sol
        self.angle_orbital = 0  # Ángulo para la órbita
        self.angle_rotacional = 0  # Rotación sobre su eje propio

        # Calcular el incremento orbital (grados por frame)
        if self.dias_sol == 0:
            self.incremento_orbital = 0
        else:
            self.incremento_orbital = 360 / (self.dias_sol * 0.5) # 0.5 segundos por día simulado

    def rotate(self):
        # Incrementar el ángulo orbital
        self.angle_orbital += math.radians(self.incremento_orbital)
        if self.angle_orbital >= 2 * math.pi:
            self.angle_orbital -= 2 * math.pi  # Reiniciar el ángulo después de una vuelta completa

        # Incrementar el ángulo de rotación sobre su eje
        self.angle_rotacional += 0.1
        if self.angle_rotacional >= 2 * math.pi:
            self.angle_rotacional -= 2 * math.pi

    def load_texture(self) -> int:
        # Cargar la textura usando Pillow
        image = Image.open(self.texture)
        img_data = image.convert("RGBA").tobytes()

        # Generar una textura en OpenGL
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # Configurar los parámetros de la textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # Cargar los datos de la textura
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            image.width, image.height, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img_data
        )

        return texture_id

    def drawPlanet(self):
        # Calcular la posición orbital
        x_position = math.cos(self.angle_orbital) * self.distancia_sol
        z_position = math.sin(self.angle_orbital) * self.distancia_sol

        # Dibujar el planeta
        glPushMatrix()
        glTranslate(x_position, 0, z_position)  # Mover el planeta a su posición orbital
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluQuadricNormals(quadric, GLU_SMOOTH)

        # Aplicar rotación sobre su eje propio
        glRotate(math.degrees(self.angle_rotacional), 0, 1, 0)

        # Dibujar la esfera del planeta
        gluSphere(quadric, self.radio, 20, 20)
        glPopMatrix()
        