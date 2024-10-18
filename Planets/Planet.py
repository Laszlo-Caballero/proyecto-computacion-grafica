from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Planeta:
    def __init__(self, nombre, masa, radio, image):
        self.nombre = nombre
        self.masa = masa
        self.radio = radio /100
        self.image_path = image
        self.texture_id = -1
        
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
        quadric = gluNewQuadric()
        gluSphere(quadric, self.radio, 60, 60)