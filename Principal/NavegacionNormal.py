from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image  
import sys
import random
import math

tamanos = {
    'Sol': 10,
    'Mercurio': 1,
    'Venus': 1.1,
    'Tierra': 1.2,
    'Marte': 1.1,
    'Júpiter': 2.5,
    'Saturno': 1.8,
    'Urano': 1.5,
    'Neptuno': 1.5,
    'Luna': 0.4
}

distancias = {
    'Mercurio': 15.0,
    'Venus': 18.0,
    'Tierra': 22.0,
    'Luna': 23.0,
    'Marte': 26.0,
    'Júpiter': 31.0,
    'Saturno': 37.0,
    'Urano': 42.0,
    'Neptuno': 47.5,
}

angulo_x = 0.0
angulo_y = 0.0
zoom = 50.0 

texturas = {}

descripciones = {
    'Sol': "El Sol: nuestra estrella",
    'Mercurio': "Mercurio: planeta más cercano al Sol",
    'Venus': "Venus: el planeta más caliente",
    'Tierra': "Tierra: nuestro hogar",
    'Luna': "Luna: nuestro satélite natural",
    'Marte': "Marte: el planeta rojo",
    'Júpiter': "Júpiter: el planeta más grande",
    'Saturno': "Saturno: conocido por sus anillos",
    'Urano': "Urano: un planeta inclinado",
    'Neptuno': "Neptuno: el planeta más alejado"
}

def cargar_textura(nombre_archivo):
    imagen = Image.open(nombre_archivo)
    imagen = imagen.transpose(Image.FLIP_TOP_BOTTOM)
    ix, iy = imagen.size
    imagen_data = imagen.convert("RGB").tobytes()
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, imagen_data)
    return textura_id
def inicializar_texturas():
    global texturas
    texturas['Sol'] = cargar_textura("texturadeplanetas/sol.jpg")
    texturas['Mercurio'] = cargar_textura("texturadeplanetas/mercurio.jpg")
    texturas['Venus'] = cargar_textura("texturadeplanetas/venus.jpg")
    texturas['Tierra'] = cargar_textura("texturadeplanetas/tierra.jpg")
    texturas['Marte'] = cargar_textura("texturadeplanetas/marte.jpg")
    texturas['Júpiter'] = cargar_textura("texturadeplanetas/jupiter.jpg")
    texturas['Saturno'] = cargar_textura("texturadeplanetas/saturno.jpg")
    texturas['Urano'] = cargar_textura("texturadeplanetas/urano.jpg")
    texturas['Neptuno'] = cargar_textura("texturadeplanetas/neptuno.jpg")
    texturas['Luna'] = cargar_textura("texturadeplanetas/luna.jpg")

def dibujar_esfera(tamano, planeta):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texturas[planeta])
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, tamano, 50, 50)
    gluDeleteQuadric(quadric)
    glDisable(GL_TEXTURE_2D)

def dibujar_descripcion(texto, x, y, z):
    glRasterPos3f(x, y, z)
    for char in texto:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))  

def dibujar_estrellas(num_estrellas):
    glBegin(GL_POINTS)
    for _ in range(num_estrellas):
        x = random.uniform(-50, 50)
        y = random.uniform(-50, 50)
        z = random.uniform(-50, 50)
        glColor3f(1.0, 1.0, 1.0)  
        glVertex3f(x, y, z)
    glEnd()
def mostrar():
    global angulo_x, angulo_y, zoom
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 0, zoom, 0, 0, 0, 0, 1, 0)
    glRotatef(angulo_x, 1, 0, 0)
    glRotatef(angulo_y, 0, 1, 0)
    dibujar_estrellas(100)
    glPushMatrix()
    dibujar_esfera(tamanos['Sol'], 'Sol')
    dibujar_descripcion(descripciones['Sol'], 0, -tamanos['Sol'] - 2, 0)  
    glPopMatrix()
    angulo_inicial = 0  
    incremento_angulo = 45 
    for planeta, distancia in distancias.items():
        angulo_rad = math.radians(angulo_inicial)
        x = distancia * math.cos(angulo_rad)
        z = distancia * math.sin(angulo_rad)
        
        glPushMatrix()
        glTranslatef(x, 0, z) 
        dibujar_esfera(tamanos[planeta], planeta)
        dibujar_descripcion(descripciones[planeta], x, -tamanos[planeta] - 2, z)  
        glPopMatrix()

        angulo_inicial += incremento_angulo  

    glutSwapBuffers()

def procesar_mouse(boton, estado, x, y):
    global zoom
    if estado == GLUT_DOWN:
        if boton == 3:  
            zoom -= 1.0
        elif boton == 4: 
            zoom += 1.0
        glutPostRedisplay()

def inicializar():
    glClearColor(0.0, 0.0, 0.0, 1.0)  
    glEnable(GL_DEPTH_TEST)  
    glPointSize(2.0)  
    inicializar_texturas() 

def cambiar_tamano(anchura, altura):
    if altura == 0:
        altura = 1
    glViewport(0, 0, anchura, altura)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(anchura) / altura, 1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def teclado(tecla, x, y):
    if tecla == b'\x1b':
        sys.exit()

def teclas_especiales(tecla, x, y):
    global angulo_x, angulo_y
    if tecla == GLUT_KEY_UP:
        angulo_x -= 5.0
    elif tecla == GLUT_KEY_DOWN:
        angulo_x += 5.0
    elif tecla == GLUT_KEY_LEFT:
        angulo_y -= 5.0
    elif tecla == GLUT_KEY_RIGHT:
        angulo_y += 5.0
    glutPostRedisplay()
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1260, 800)
    glutCreateWindow(b"Sistema Solar 3D - OpenGL")
    inicializar()
    glutDisplayFunc(mostrar)
    glutReshapeFunc(cambiar_tamano)
    glutKeyboardFunc(teclado)
    glutSpecialFunc(teclas_especiales)
    glutMouseFunc(procesar_mouse) 
    glutMainLoop()
if __name__ == "__main__":
    main()
