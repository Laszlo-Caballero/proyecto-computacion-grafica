from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Planets.Planet import Planeta

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.sol = Planeta("sol", 2000, 20, "sol.bmp")
        
        

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
        gluLookAt(2.5, 1.0, 2.5,  # Posición de la cámara
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