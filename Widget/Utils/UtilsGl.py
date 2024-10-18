from PyQt5.QtWidgets import QOpenGLWidget 
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def get_center_of_window(self: QOpenGLWidget):
        # Obtener la geometría de la ventana (posición y tamaño)
    window_geometry = self.geometry()

        # Calcular el centro de la ventana
    center_x = window_geometry.x() + window_geometry.width() // 2
    center_y = window_geometry.y() + window_geometry.height() // 2

    return (center_x, center_y)

def GetCameraPosition(camera_distance, camera_yaw, camera_pitch):
    yaw_radians = math.radians(camera_yaw)
    pitch_radians = math.radians(camera_pitch)
    camera_x = camera_distance * math.cos(pitch_radians) * math.sin(yaw_radians)
    camera_y = camera_distance * math.sin(pitch_radians)
    camera_z = camera_distance * math.cos(pitch_radians) * math.cos(yaw_radians)
    return (camera_x, camera_y, camera_z)



def draw_axes():
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