from PIL import Image
import os


archivos = os.listdir("utils\images")

for imagen in archivos:
    opImagen = Image.open(imagen)
    

print(archivos)