# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL CREATIVE
# Archivo .vdr ejecutado nativamente para Blender

import bpy
import bmesh
import mathutils
from mathutils import Vector

class VaderBlenderCreative:
    def __init__(self):
        self.scene = bpy.context.scene
        print("🎨 VADER 7.0 - Blender Creative Runtime")
    
    def crear_cubo(self, location=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add(location=location)
        return bpy.context.active_object
    
    def crear_esfera(self, location=(0, 0, 0), radius=1):
        bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=radius)
        return bpy.context.active_object
    
    def crear_luz(self, location=(0, 0, 5), energy=10):
        bpy.ops.object.light_add(type='SUN', location=location)
        light = bpy.context.active_object
        light.data.energy = energy
        return light
    
    def crear_camara(self, location=(7, -7, 5)):
        bpy.ops.object.camera_add(location=location)
        return bpy.context.active_object
    
    def animar_rotacion(self, objeto, frames=250):
        objeto.rotation_euler = (0, 0, 0)
        objeto.keyframe_insert(data_path="rotation_euler", frame=1)
        objeto.rotation_euler = (0, 0, 6.28)
        objeto.keyframe_insert(data_path="rotation_euler", frame=frames)

def ejecutar_escena_vader():
    vader = VaderBlenderCreative()
    
    cubo = vader.crear_cubo(location=(0, 0, 0))
    esfera = vader.crear_esfera(location=(3, 0, 0))
    luz = vader.crear_luz(location=(5, 5, 5))
    camara = vader.crear_camara()
    if "cubo" in locals(): vader.animar_rotacion(cubo)
    print("✅ Escena Vader creada en Blender")

if __name__ == "__main__":
    ejecutar_escena_vader()
