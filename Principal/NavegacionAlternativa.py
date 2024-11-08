from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import sys
import random
import math

tamanos = {
    'Sol': 10, 'Mercurio': 1, 'Venus': 1.1, 'Tierra': 1.2, 'Marte': 1.1,
    'Júpiter': 2.5, 'Saturno': 1.8, 'Urano': 1.5, 'Neptuno': 1.5, 'Luna': 0.4
}

posiciones = {
    'Sol': (0, 0, 0), 'Mercurio': (15, 0, 0), 'Venus': (18, 0, 0), 'Tierra': (22, 0, 0),
    'Luna': (23, 0, 1), 'Marte': (26, 0, 0), 'Júpiter': (31, 0, 0),
    'Saturno': (37, 0, 0), 'Urano': (42, 0, 0), 'Neptuno': (47.5, 0, 0)
}

cam_x, cam_y, cam_z = 0.0, 0.0, 40.0  
zoom_nivel = 40.0  
angulo_yaw, angulo_pitch = 0.0, 0.0
texturas, planeta_seleccionado = {}, None
mouse_x, mouse_y = 0, 0
arrastrando = False

def cargar_textura(nombre_archivo):
    try:
        imagen = Image.open(nombre_archivo).transpose(Image.FLIP_TOP_BOTTOM)
        ix, iy = imagen.size
        imagen_data = imagen.convert("RGB").tobytes()
        
        textura_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textura_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, imagen_data)
        return textura_id
    except FileNotFoundError:
        print(f"Error: No se pudo cargar la textura '{nombre_archivo}'")
        return None

def inicializar_texturas():
    global texturas
    nombres_texturas = {
        'Sol': "texturadeplanetas/sol.jpg", 'Mercurio': "texturadeplanetas/mercurio.jpg",
        'Venus': "texturadeplanetas/venus.jpg", 'Tierra': "texturadeplanetas/tierra.jpg",
        'Marte': "texturadeplanetas/marte.jpg", 'Júpiter': "texturadeplanetas/jupiter.jpg",
        'Saturno': "texturadeplanetas/saturno.jpg", 'Urano': "texturadeplanetas/urano.jpg",
        'Neptuno': "texturadeplanetas/neptuno.jpg", 'Luna': "texturadeplanetas/luna.jpg"
    }
    for planeta, archivo in nombres_texturas.items():
        textura = cargar_textura(archivo)
        if textura:
            texturas[planeta] = textura

def dibujar_esfera(tamano, planeta):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texturas[planeta])
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, tamano, 50, 50)
    gluDeleteQuadric(quadric)
    glDisable(GL_TEXTURE_2D)
def dibujar_estrellas(num_estrellas):
    glBegin(GL_POINTS)
    for _ in range(num_estrellas):
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(random.uniform(-50, 50), random.uniform(-50, 50), random.uniform(-50, 50))
    glEnd()

def mostrar():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -zoom_nivel) 
    glRotatef(angulo_pitch, 1, 0, 0)
    glRotatef(angulo_yaw, 0, 1, 0)
    glTranslatef(-cam_x, -cam_y, -cam_z)
    
    dibujar_estrellas(100)

    for planeta, tamano in tamanos.items():
        glPushMatrix()
        x, y, z = posiciones[planeta]
        glTranslatef(x, y, z)
        dibujar_esfera(tamano, planeta)
        glPopMatrix()

    dibujar_cabina()
    dibujar_texto_superior("Nave Espacial N° 001")
    dibujar_boton_reinicio()
    glutSwapBuffers()

def dibujar_cabina():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT), -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    ancho, alto = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    borde = 30
    
    glColor4f(0.1, 0.1, 0.2, 0.85)  
    glBegin(GL_QUADS)
    glVertex2f(0, alto)
    glVertex2f(ancho, alto)
    glVertex2f(ancho, alto - borde)
    glVertex2f(0, alto - borde)
    glVertex2f(0, 0)
    glVertex2f(ancho, 0)
    glVertex2f(ancho, borde)
    glVertex2f(0, borde)
    glVertex2f(0, alto)
    glVertex2f(borde, alto)
    glVertex2f(borde, 0)
    glVertex2f(0, 0)
    glVertex2f(ancho - borde, alto)
    glVertex2f(ancho, alto)
    glVertex2f(ancho, 0)
    glVertex2f(ancho - borde, 0)
    glEnd()

    if planeta_seleccionado:
        glColor3f(0.5, 1, 0.5)  
        glWindowPos2f(30, alto - 50)
        for char in f"Planeta más cercano: {planeta_seleccionado}":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def dibujar_texto_superior(texto):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT), -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    ancho, alto = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    glColor3f(0.8, 0.8, 1)  
    glWindowPos2f(ancho / 2 - 70, alto - 30)  
    
    for char in texto:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def dibujar_boton_reinicio():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT), -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    ancho, alto = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    boton_x, boton_y = ancho - 120, 20  
    
    glColor3f(0.3, 0.3, 0.9)  
    glBegin(GL_QUADS)
    glVertex2f(boton_x, boton_y)
    glVertex2f(boton_x + 100, boton_y)
    glVertex2f(boton_x + 100, boton_y + 30)
    glVertex2f(boton_x, boton_y + 30)
    glEnd()
    
    glColor3f(1, 1, 1)  
    glWindowPos2f(boton_x + 15, boton_y + 8)
    for char in "Reiniciar":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def procesar_clic_mouse(boton, estado, x, y):
    global cam_x, cam_y, cam_z, zoom_nivel, angulo_yaw, angulo_pitch, arrastrando, mouse_x, mouse_y
    ancho, alto = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    boton_x, boton_y = ancho - 120, 20  
    
    if boton == GLUT_LEFT_BUTTON and estado == GLUT_DOWN:
        if boton_x <= x <= boton_x + 100 and alto - boton_y <= y <= alto - boton_y + 30:
            cam_x, cam_y, cam_z = 0.0, 0.0, 40.0
            zoom_nivel = 40.0  
            angulo_yaw, angulo_pitch = 0.0, 0.0
            glutPostRedisplay()
        else:
            arrastrando = True
            mouse_x, mouse_y = x, y
    elif boton == GLUT_LEFT_BUTTON and estado == GLUT_UP:
        arrastrando = False
def mover_raton(x, y):
    global angulo_yaw, angulo_pitch, mouse_x, mouse_y, arrastrando
    if arrastrando:
        dx, dy = x - mouse_x, y - mouse_y
        angulo_yaw += dx * 0.1
        angulo_pitch -= dy * 0.1
        mouse_x, mouse_y = x, y
        glutPostRedisplay()

def zoom_wheel(button, direction, x, y):
    global zoom_nivel
    if direction > 0:  # Zoom in
        zoom_nivel = max(zoom_nivel - 2, 1)  
    elif direction < 0:  # Zoom out
        zoom_nivel = min(zoom_nivel + 2, 150)  
    glutPostRedisplay()

def teclas_especiales(tecla, x, y):
    global cam_x, cam_y, cam_z
    velocidad = 0.5
    if tecla == GLUT_KEY_UP:
        cam_z -= velocidad  
    elif tecla == GLUT_KEY_DOWN:
        cam_z += velocidad  
    elif tecla == GLUT_KEY_LEFT:
        cam_x -= velocidad  
    elif tecla == GLUT_KEY_RIGHT:
        cam_x += velocidad  
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
    gluPerspective(45, float(anchura) / altura, 1, 200.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1260, 800)
    glutCreateWindow(b"Sistema Solar 3D - Nave Espacial")
    inicializar()
    glutDisplayFunc(mostrar)
    glutReshapeFunc(cambiar_tamano)
    glutMouseFunc(procesar_clic_mouse)
    glutMotionFunc(mover_raton)
    glutMouseWheelFunc(zoom_wheel)
    glutSpecialFunc(teclas_especiales)
    glutMainLoop()

