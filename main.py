import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Widget.GLWidget import GLWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt
from Widget.GLWidget import GLWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QBrush

class WelcomeScreen(QWidget):
    def __init__(self, show_solar_system_callback):
        super().__init__()
        self.initUI(show_solar_system_callback)
    def initUI(self, show_solar_system_callback):
        self.set_background_image(r'assets/images.jpeg')     
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        welcome_label = QLabel("Bienvenido a *CONOCE EL SISTEMA SOLAR*", self)
        welcome_label.setFont(QFont("Arial", 28, QFont.Bold))
        welcome_label.setStyleSheet("color: white;")
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

    def set_background_image(self, image_path):
        absolute_path = os.path.abspath(image_path)
        print(f"Intentando cargar la imagen desde: {absolute_path}")

        pixmap = QPixmap(absolute_path)
        if pixmap.isNull():
            print(f"Error al cargar la imagen desde: {absolute_path}.")
            return
        
        print("Imagen cargada correctamente.")
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)
        
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 1000)
        self.setWindowTitle("Simulación del Sistema Solar")
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