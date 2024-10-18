import sys
from PyQt5.QtGui import QMouseEvent, QWheelEvent, QPainter, QFont
from PyQt5.QtWidgets import QOpenGLWidget, QPushButton
from PyQt5.QtCore import Qt
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
        self.show_box = False
        self.mouse_is_press = False
        self.button = QPushButton("Cerrar", self)
        self.button.clicked.connect(self.toggle_info_box)
        self.button.hide()
        
    def toggle_info_box(self):
        self.show_box = not self.show_box 
        if not self.show_box:  # Si el recuadro no se va a mostrar, oculta el botón
            self.button.hide()
        else:  # Si el recuadro se va a mostrar, muestra el botón
            self.button.show()
        self.update()  
        
    def get_center_of_window(self):
        # Obtener la geometría de la ventana (posición y tamaño)
        window_geometry = self.geometry()

        # Calcular el centro de la ventana
        center_x = window_geometry.x() + window_geometry.width() // 2
        center_y = window_geometry.y() + window_geometry.height() // 2

        return (center_x, center_y)

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
        # self.sol.load_texture()
        # glBindTexture(GL_TEXTURE_2D, self.sol.texture_id)
        # self.sol.drawPlanet()
        
        
        self.draw_axes()
        
        if self.show_box:
            self.draw_info_box()

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
    
    def draw_info_box(self):
        
        # Dibujar el recuadro en la esquina superior derecha
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.setBrush(Qt.black)
        painter.drawRect(self.width() - 300, 10, 290, 200)  
        painter.setFont(QFont("Arial", 10))
        painter.drawText(self.width() - 290, 30, "ola :D")  
        
        self.button.setGeometry(self.width()  - 290, 170, 80, 30)  
        self.button.show()  
        painter.end()   

    def mouseMoveEvent(self, event: QMouseEvent | None):        
        center_x, center_y = self.get_center_of_window()
        if self.mouse_is_press:
            x = event.pos().x() - center_x
            y = event.pos().y() - center_y

        print(f"Mouse clicked at: x={x}, y={y}")
        
        
    def wheelEvent(self, event: QWheelEvent | None):
        delta = event.angleDelta().y()
        
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    
    def mousePressEvent(self, event: QMouseEvent | None):
        if event.button() == Qt.LeftButton:
            self.mouse_is_press = True
            self.show_box = True  # Mostrar el recuadro al hacer clic
            self.update() 
            
    def mouseReleaseEvent(self, event: QMouseEvent | None):
        if event.button() == Qt.LeftButton:
            self.mouse_is_press = False
        