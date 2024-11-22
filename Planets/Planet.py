from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
from pygltflib import GLTF2
import numpy as np

class Planeta:
    def __init__(self, nombre, radio, obj, distancia_sol, dias_Sol):
        self.nombre = nombre
        self.radio = radio / 100
        self.obj = GLTF2().load(f"obj/{obj}")
        self.texture_id = -1
        self.distancia_sol = distancia_sol
        self.dia_Sol = dias_Sol
        self.z = 0
        segundos = self.dia_Sol * 60 / 365
        if dias_Sol == 0:
            self.angle_increment = 0
        else:
            self.angle_increment = (2 * math.pi) / (segundos * (1000 / 16))

    def rotate(self):
        self.z += self.angle_increment

    def cargarVertices(self):
        obj = self.obj
        
        # Obtener el accesor de los vértices
        accesor = obj.accessors[obj.meshes[0].primitives[0].attributes.POSITION]
        print("Accesor:", accesor)

        # Obtener el bufferView
        buffer_view = obj.bufferViews[accesor.bufferView]
        print("Buffer View:", buffer_view)

        # Obtener el buffer
        buffer = obj.buffers[buffer_view.buffer]
        print("Buffer:", buffer)

        # Leer los datos binarios
        if buffer.uri is None:
            raise ValueError("El archivo GLB no contiene datos binarios o el URI está vacío.")
        
        if buffer.uri.startswith("data:"):
            # Si los datos están embebidos en el archivo GLB (data-uri)
            binary_data = np.frombuffer(bytes(buffer.uri.split(",")[1], "utf-8"), dtype=np.uint8)
        else:
            # Si los datos están en un archivo externo
            file_path = os.path.join(os.path.dirname(self.obj.uri), buffer.uri)
            with open(file_path, "rb") as f:
                binary_data = np.frombuffer(f.read(), dtype=np.uint8)
        
        start = buffer_view.byteOffset
        end = start + buffer_view.byteLength
        
        vertex_data = np.frombuffer(binary_data[start:end], dtype=np.float32)
        vertices = vertex_data.reshape((-1, 3))
        
        return vertices

    def drawPlanet(self):
        x_position = math.cos(self.z) * self.distancia_sol
        z_position = math.sin(self.z) * self.distancia_sol
        
        glTranslatef(x_position, 0, z_position)
        
        vertices = self.cargarVertices()
        
        glBegin(GL_TRIANGLES)
        for vertex in vertices:
            glVertex3fv(vertex)
        glEnd()
        glutSwapBuffers()

        