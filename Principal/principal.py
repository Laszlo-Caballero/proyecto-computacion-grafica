import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt
import NavegacionAlternativa  
import NavegacionNormal  
# Formulario 1
class FormularioInicio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Explora el Sistema Solar")
        self.setGeometry(100, 100, 1200, 800)  
        fondo = QPixmap("bienvenida/iniciando.jpg")
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(fondo))
        self.setPalette(palette)
        btn_empezar = QPushButton("EMPEZAR AHORA", self)
        btn_empezar.setStyleSheet("background-color: #ffcc00; color: #000; font-size: 18px; font-weight: bold; padding: 10px 20px; border-radius: 10px;")
        btn_empezar.setFont(QFont('Arial', 16))
        btn_empezar.setGeometry(505, 650, 250, 60)  
        btn_empezar.clicked.connect(self.mostrar_formulario_opciones)
    def mostrar_formulario_opciones(self):
        self.hide()
        self.formulario_opciones = FormularioOpciones()
        self.formulario_opciones.show()

# Formulario 2
class FormularioOpciones(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opciones de Navegación")
        self.setGeometry(100, 100, 1260, 800)  
        fondo = QPixmap("bienvenida/seleccion.jpg").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(fondo))
        self.setPalette(palette)
        btn_navegacion_normal = QPushButton("Navegación Normal", self)
        btn_navegacion_normal.setStyleSheet("background-color: #4CAF50; color: #FFF; font-size: 18px; font-weight: bold; padding: 10px 20px; border-radius: 10px;")
        btn_navegacion_normal.setFont(QFont('Arial', 14))
        btn_navegacion_normal.setGeometry(400, 600, 250, 60)  

        btn_navegacion_alterna = QPushButton("Navegación Alterna", self)
        btn_navegacion_alterna.setStyleSheet("background-color: #2196F3; color: #FFF; font-size: 18px; font-weight: bold; padding: 10px 20px; border-radius: 10px;")
        btn_navegacion_alterna.setFont(QFont('Arial', 14))
        btn_navegacion_alterna.setGeometry(660, 600, 250, 60) 
        btn_navegacion_normal.clicked.connect(self.navegacion_normal)
        btn_navegacion_alterna.clicked.connect(self.navegacion_alterna)

    def resizeEvent(self, event):
        fondo = QPixmap("bienvenida/seleccion.jpg").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(fondo))
        self.setPalette(palette)
        super().resizeEvent(event)

    def navegacion_normal(self):
        print("Navegación Normal seleccionada.")
        NavegacionNormal.main()  

    def navegacion_alterna(self):
        print("Navegación Alterna seleccionada.")
        NavegacionAlternativa.main()  

#principal
app = QApplication(sys.argv)
formulario_inicio = FormularioInicio()
formulario_inicio.show()
sys.exit(app.exec_())
