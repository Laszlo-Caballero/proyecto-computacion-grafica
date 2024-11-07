import random
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Widget.GLWidget import GLWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont,QPalette, QColor, QPainter
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class WelcomeScreen(QWidget):
    def __init__(self, show_solar_system_callback):
        super().__init__()
        self.initUI(show_solar_system_callback)
        
        self.star_positions = [(random.randint(0, 1200), random.randint(100, 1000)) for _ in range(100)]  
        self.planet_positions = [(i * 200 + 100, 500) for i in range(5)]  
        self.moon_positions = [(i * 150 + 50, 550) for i in range(8)]  
        self.sun_position = (540, 50)  

    def initUI(self, show_solar_system_callback):

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 50))  
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel("CONOCE EL SISTEMA SOLAR", self)
        welcome_label.setFont(QFont("Arial", 55, QFont.Bold))
        welcome_label.setStyleSheet("color: gold;")
        welcome_label.setAlignment(Qt.AlignCenter)

        observe_button = QPushButton("Observar Sistema Solar", self)
        observe_button.setFont(QFont("Arial", 16))
        observe_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        observe_button.clicked.connect(show_solar_system_callback)

        layout.addWidget(welcome_label)
        layout.addWidget(observe_button)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)

        self.draw_starry_background(painter)

    def draw_starry_background(self, painter):
        painter.setBrush(QColor(25, 25, 112))  
        painter.drawRect(0, 0, self.width(), self.height())  
        painter.setBrush(QColor(255, 255, 255))  
        for pos in self.star_positions:
            painter.drawEllipse(pos[0], pos[1], 2, 2)  
        planet_colors = [QColor(50, 205, 50), QColor(255, 69, 50), QColor(65, 105, 225), QColor(255, 215, 1), QColor(138, 43, 226)]
        for i, pos in enumerate(self.planet_positions):
            painter.setBrush(planet_colors[i % len(planet_colors)])  
            painter.drawEllipse(pos[0], pos[1], 100, 100) 
        painter.setBrush(QColor(169, 169, 169))  
        for pos in self.moon_positions:
            painter.drawEllipse(pos[0], pos[1], 30, 30) 
        painter.setBrush(QColor(255, 255, 0))  
        painter.drawEllipse(self.sun_position[0], self.sun_position[1], 240, 250)  

def show_solar_system():
    print("Observando el sistema solar...")  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 1000)
        self.setWindowTitle("Simulación del Sistema Solar")
        self.gl_widget = GLWidget(self)
        self.stacked_widget = QStackedWidget(self)
        self.welcome_screen = WelcomeScreen(self.show_solar_system)
        self.stacked_widget.addWidget(self.welcome_screen)
        self.opengl_widget = GLWidget(self)
        self.stacked_widget.addWidget(self.opengl_widget)
        self.setCentralWidget(self.stacked_widget)
    def show_solar_system(self):
        self.stacked_widget.setCurrentWidget(self.opengl_widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
window = WelcomeScreen(show_solar_system)
window.resize(800, 600)  