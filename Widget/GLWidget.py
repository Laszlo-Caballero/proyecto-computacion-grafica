from PyQt5.QtGui import QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import  QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Planets.Planet import Planeta
from .Utils.UtilsGl import GetCameraPosition, draw_axes

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.sol = Planeta("sol", 2000, 20, "sol.bmp")
        self.zoom_factor = 1.0
        self.camera_distance = 5.0
        self.mouse_is_press = False
        self.camera_yaw = 0.0  # Rotación horizontal (eje Y)
        self.camera_pitch = 0.0  # Rotación vertical (eje X)
        self.last_mouse_pos = None  # Última posición del mouse
        
    def reshape(width, height):
        if height == 0:
            height = 1
        aspect = width / height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
      
    def zoom_in(self):
        self.camera_distance *= 0.9
        self.update()

    def zoom_out(self):
        self.camera_distance *= 1.1  # Aumenta el factor de zoom para alejar
        self.update()

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
        
        camera_x, camera_y, camera_z = GetCameraPosition(self.camera_distance, self.camera_yaw, self.camera_pitch)

    
        gluLookAt(camera_x, camera_y, camera_z,  # Posición de la cámara ajustada
                  0, 0, 0,  # Mira hacia (centro de la escena)
                  0.0, 1.0, 0)
        self.sol.load_texture()
        glBindTexture(GL_TEXTURE_2D, self.sol.texture_id)
        self.sol.drawPlanet()
        
        
        draw_axes()
        
    def wheelEvent(self, event: QWheelEvent | None):
        delta = event.angleDelta().y()
        
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    
    def mousePressEvent(self, event: QMouseEvent | None):
        if event.button() == Qt.LeftButton:
            self.mouse_is_press = True
    
    def mouseReleaseEvent(self, event: QMouseEvent | None):
        if event.button() == Qt.LeftButton:
            self.mouse_is_press = False

    
    
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.mouse_is_press:
        # Obtener la posición actual del mouse
            current_pos = event.pos()
        
            if self.last_mouse_pos is not None:
            # Calcular el desplazamiento del mouse
                delta_x = current_pos.x() - self.last_mouse_pos.x()
                delta_y = current_pos.y() - self.last_mouse_pos.y()

            # Ajustar los ángulos de rotación basados en el desplazamiento del mouse
                self.camera_yaw += delta_x * 0.5  # Ajusta la sensibilidad de rotación
                self.camera_pitch -= delta_y * 0.5  # Ajusta la sensibilidad de rotación

            # Limitar la rotación vertical para evitar que la cámara se voltee completamente
                self.camera_pitch = max(-89, min(89, self.camera_pitch))  # Limitar pitch entre -89 y 89 grados
        
        # Actualizar la última posición del mouse
            self.last_mouse_pos = current_pos

        # Actualizar la escena
            self.update()
            
            
    def mousePressEvent(self, event: QMouseEvent):
         if event.button() == Qt.LeftButton:
            self.mouse_is_press = True
            self.last_mouse_pos = event.pos()  # Almacenar la posición del mouse al presionar

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.mouse_is_press = False
            self.last_mouse_pos = None  # Reiniciar la posición del mouse al soltar