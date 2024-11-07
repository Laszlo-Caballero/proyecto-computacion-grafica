from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class Planeta:
    def __init__(self, nombre, radio, image, distancia_sol, dias_Sol):
        self.nombre = nombre
        self.radio = radio /100
        self.image_path = image
        self.texture_id = -1
        self.distancia_sol = distancia_sol
        self.dia_Sol = dias_Sol
        self.z = 0
        segundos = self.dia_Sol * 60/365
        if dias_Sol == 0:
            self.angle_increment = 0
        else:
            self.angle_increment = (2 * math.pi) / (segundos * (1000 / 16))
        
     
     
    def rotate(self):
        self.z += self.angle_increment
        
    def load_texture(self):
        try:
            img = Image.open(f"./assets/{self.image_path}")
            img_data = img.convert("RGBA").tobytes()
            width, height = img.size
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        except Exception as e:
            print(f"Error al cargar textura: {e}")
    
    def drawPlanet(self):
        
        x_position = math.cos(self.z) * self.distancia_sol
        z_position = math.sin(self.z) * self.distancia_sol
        
        glTranslate(x_position, 0, z_position)
        quadric = gluNewQuadric()
        gluSphere(quadric, self.radio, 60, 60)