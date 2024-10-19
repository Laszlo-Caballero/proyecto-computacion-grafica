from PyQt5.QtGui import QKeyEvent, QMouseEvent, QWheelEvent, QPainter, QFont
from PyQt5.QtWidgets import QOpenGLWidget, QPushButton
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Planets.Planet import Planeta
from .Utils.UtilsGl import GetCameraPosition, draw_axes
from utils.planetas import planetasObj

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.sol = Planeta("sol", 20, "sol.bmp", 0)
        self.mercurio = Planeta("mercurio", 10, "", 1.5)
        self.zoom_factor = 1.0
        self.camera_distance = 5.0
        self.mouse_is_press = False
        self.camera_yaw = 0.0  # Rotación horizontal (eje Y)
        self.camera_pitch = 0.0  # Rotación vertical (eje X)
        self.last_mouse_pos = None  # Última posición del mouse
        self.show_box = False
        self.mouse_is_press = False
        self.button = QPushButton("Cerrar", self)
        self.button.clicked.connect(self.toggle_info_box)
        self.button.hide()
        self.setFocusPolicy(Qt.StrongFocus)
        self.center_camera_x = 0
        self.center_camera_y = 0
        
        self.PlanetasClass: list[Planeta] = []

        for planeta in planetasObj:
            newPlanet = Planeta(planeta, planetasObj[planeta]["tamaño"], planetasObj[planeta]["textura"],
                        planetasObj[planeta]["distancia"])
            self.PlanetasClass.append(newPlanet)
        
    def toggle_info_box(self):
        self.show_box = not self.show_box 
        if not self.show_box:  # Si el recuadro no se va a mostrar, oculta el botón
            self.button.hide()
        else:  # Si el recuadro se va a mostrar, muestra el botón
            self.button.show()
        self.update()  
        
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
                  self.center_camera_x, self.center_camera_y, 0,  # Mira hacia (centro de la escena)
                  0.0, 1.0, 0)
        # self.sol.load_texture()
        # glBindTexture(GL_TEXTURE_2D, self.sol.texture_id)
        # self.sol.drawPlanet()
        
        
        # self.mercurio.drawPlanet()
        
        for planeta in self.PlanetasClass:
            # planeta.load_texture()
            # glBindTexture(GL_TEXTURE_2D, planeta.texture_id)
            planeta.drawPlanet()
            
            
        
        
        # draw_axes()
        
        if self.show_box:
            self.draw_info_box()
        
    def draw_info_box(self):
        
        # Dibujar el recuadro en la esquina superior derecha
        painter = QPainter(self)
        painter.setPen(Qt.white)
        painter.setBrush(Qt.black)
        painter.drawRect(self.width() - 300, 10, 290, 200)  
        painter.setFont(QFont("Arial", 10))
        painter.drawText(self.width() - 290, 30, "INFO PLANETA")  
        
        self.button.setGeometry(self.width()  - 290, 170, 80, 30)  
        self.button.show()  
        painter.end() 
    
    def wheelEvent(self, event: QWheelEvent | None):
        delta = event.angleDelta().y()
        
        if delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
    
    

    
    
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
        self.show_box = True
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.mouse_is_press = False
            self.last_mouse_pos = None  # Reiniciar la posición del mouse al soltar
    
    def keyPressEvent(self, event: QKeyEvent | None):
        key = event.key()
        print(key)
    # Mover la cámara en pasos dependiendo de la tecla presionada
        step = 0.2
        if key == Qt.Key_A:  # Mover a la izquierda
            self.center_camera_x -= step
        elif key == Qt.Key_S:  # Mover hacia abajo
            self.center_camera_y -= step
        elif key == Qt.Key_W:
            self.center_camera_y += step
        elif key == Qt.Key_D:  # Mover a la derecha
            self.center_camera_x += step
            
        self.update()
