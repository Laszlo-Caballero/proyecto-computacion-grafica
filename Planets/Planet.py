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
        self.dia_Sol = dias_Sol
        self.z = 0
        segundos = self.dia_Sol * 60 / 365
        if dias_Sol == 0:
            self.angle_increment = 0
        else:
            self.angle_increment = (2 * math.pi) / (segundos * (1000 / 16))

    def rotate(self):
        self.z += self.angle_increment



    def load_texture(self) -> int:
         # Cargar la textura usando Pillow
         image = Image.open(self.texture)  # Flip porque OpenGL usa coordenadas inversas
         img_data = image.convert("RGBA").tobytes()

         # Generar una textura en OpenGL
         texture_id = glGenTextures(1)
         glBindTexture(GL_TEXTURE_2D, texture_id)

    #     # Configurar los parámetros de la textura
         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
    #     # Cargar los datos de la textura
         glTexImage2D(
             GL_TEXTURE_2D, 0, GL_RGBA,
             image.width, image.height, 0,
             GL_RGBA, GL_UNSIGNED_BYTE, img_data
         )

         return texture_id

    def drawPlanet(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        x_position = math.cos(self.z) * self.distancia_sol
        z_position = math.sin(self.z) * self.distancia_sol
        
        glTranslate(x_position, 0, z_position)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluSphere(quadric, self.radio, 20, 20)
        
        
        
        