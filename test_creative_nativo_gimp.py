# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL CREATIVE
# Archivo .vdr ejecutado nativamente para GIMP

from gimpfu import *

def ejecutar_proyecto_vader():
    print("🎨 VADER 7.0 - GIMP Creative Runtime")
    imagen = pdb.gimp_image_new(1920, 1080, RGB)
    capa = pdb.gimp_layer_new(imagen, 1920, 1080, RGBA_IMAGE, "Capa Vader", 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(imagen, capa, None, 0)
    pdb.gimp_display_new(imagen)
    print("✅ Proyecto GIMP creado")

register("python_fu_vader", "Vader Creative", "Proyecto Vader", "Vader", "Vader", "2025", 
         "<Image>/Filters/Vader/Creative", "*", [], [], ejecutar_proyecto_vader)
main()
