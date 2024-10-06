import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Planets.Planet import Planeta

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.sol = Planeta("sol", 2000, 20, "sol.bmp")
        self.zoom_factor = 1.0
        self.camera_x = 2.5
        self.camera_y = 1.0
        self.camera_z = 2.5
        
    def zoom_in(self):
        self.zoom_factor *= 0.9  # Reduce el factor de zoom para acercar
        self.update_camera_position()
        self.update()

    def zoom_out(self):
        self.zoom_factor *= 1.1  # Aumenta el factor de zoom para alejar
        self.update_camera_position()
        self.update()
    def update_camera_position(self):
        self.camera_x = 2.5 * self.zoom_factor
        self.camera_y = 1.0 * self.zoom_factor
        self.camera_z = 2.5 * self.zoom_factor

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)       
        glMatrixMode(GL_PROJECTION)
        glutInit()
        glEnable(GL_TEXTURE_2D)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / h if h != 0 else 1, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(self.camera_x, self.camera_y, self.camera_z,  # Posición de la cámara ajustada
                  0, 0, 0,  # Mira hacia (centro de la escena)
                  0.0, 1.0, 0)
        self.sol.load_texture()
        glBindTexture(GL_TEXTURE_2D, self.sol.texture_id)
        self.sol.drawPlanet()
        
        
        self.draw_axes()

    def draw_axes(self):
        glColor3f(1.0, 1.0, 1.0)  
        glBegin(GL_LINES)  
        #Eje X
        glVertex3f(-1.0, 0.0, 0.0)  
        glVertex3f(1.0, 0.0, 0.0)  
        

        #Eje Y
        glVertex3f(0.0, -1.0, 0.0)  
        glVertex3f(0.0, 1.0, 0.0) 
        #Eje Z
        glVertex3f(0.0, 0.0, -1.0) 
        glVertex3f(0.0, 0.0, 1.0) 
        glEnd() 
        
        
        
        glRasterPos3f(1.2,0.0,0.0)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord("X"))
        glRasterPos3f(-1.2,0.0,0.0)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord("X"))
        glRasterPos3f(0.0,1.2,0.0)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord("Y"))
        glRasterPos3f(0.0,-1.2,0.0)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord("Y"))
        glRasterPos3f(0.0,0.0,1.2)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord("Z"))
        glRasterPos3f(0.0,0.0,-1.2)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord("Z"))
        
    