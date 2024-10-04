import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Widget.GLWidget import GLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200,1000)
        self.setWindowTitle("Simulacion de")
        self.opengl_widget = GLWidget(self)
        self.setCentralWidget(self.opengl_widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()
        

sys.exit(app.exec_())        
