#!/usr/bin/env python3
"""
Generador de Aplicaciones Electron desde Vader
Crea aplicaciones Electron completas a partir de archivos .vdr
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transpilers.electron import ElectronTranspiler

def generar_aplicacion_electron(archivo_vdr, directorio_salida):
    """
    Genera una aplicación Electron completa desde un archivo .vdr
    """
    print(f"🚀 Generando aplicación Electron desde: {archivo_vdr}")
    
    # Leer el archivo Vader
    try:
        with open(archivo_vdr, 'r', encoding='utf-8') as f:
            codigo_vader = f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se pudo encontrar el archivo {archivo_vdr}")
        return False
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return False
    
    # Crear el directorio de salida
    try:
        os.makedirs(directorio_salida, exist_ok=True)
        print(f"📁 Directorio de salida creado: {directorio_salida}")
    except Exception as e:
        print(f"❌ Error al crear directorio: {e}")
        return False
    
    # Transpilar con Electron
    try:
        transpiler = ElectronTranspiler()
        archivos_generados = transpiler.transpile(codigo_vader)
        print(f"✅ Transpilación completada. {len(archivos_generados)} archivos generados.")
    except Exception as e:
        print(f"❌ Error durante la transpilación: {e}")
        return False
    
    # Guardar todos los archivos generados
    archivos_creados = []
    for nombre_archivo, contenido in archivos_generados.items():
        ruta_archivo = os.path.join(directorio_salida, nombre_archivo)
        
        try:
            # Crear directorios padre si no existen
            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
            
            # Guardar el archivo
            if nombre_archivo == 'package.json':
                # Para package.json, el contenido ya es un string JSON
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
            else:
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
            
            archivos_creados.append(nombre_archivo)
            print(f"  ✅ {nombre_archivo}")
            
        except Exception as e:
            print(f"  ❌ Error al guardar {nombre_archivo}: {e}")
    
    # Copiar assets si existen
    copiar_assets(directorio_salida)
    
    # Mostrar instrucciones de instalación
    mostrar_instrucciones(directorio_salida)
    
    print(f"\n🎉 ¡Aplicación Electron generada exitosamente!")
    print(f"📍 Ubicación: {directorio_salida}")
    print(f"📄 Archivos creados: {len(archivos_creados)}")
    
    return True

def copiar_assets(directorio_salida):
    """Copia assets necesarios como logos e iconos"""
    try:
        # Buscar el logo de Vader
        vader_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logo_paths = [
            os.path.join(vader_dir, 'assets', 'logo.png'),
            os.path.join(vader_dir, 'assets', 'icons', 'vader-logo.png'),
            os.path.join(vader_dir, 'vscode_extension', 'logo.png')
        ]
        
        assets_dir = os.path.join(directorio_salida, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                shutil.copy2(logo_path, os.path.join(assets_dir, 'logo.png'))
                print(f"  ✅ Logo copiado desde: {logo_path}")
                break
        else:
            print("  ⚠️  Logo de Vader no encontrado")
            
    except Exception as e:
        print(f"  ⚠️  Error al copiar assets: {e}")

def mostrar_instrucciones(directorio_salida):
    """Muestra las instrucciones para ejecutar la aplicación"""
    print(f"\n📋 INSTRUCCIONES PARA EJECUTAR LA APLICACIÓN:")
    print(f"")
    print(f"1. Navegar al directorio:")
    print(f"   cd {directorio_salida}")
    print(f"")
    print(f"2. Instalar dependencias:")
    print(f"   npm install")
    print(f"")
    print(f"3. Ejecutar en modo desarrollo:")
    print(f"   npm start")
    print(f"")
    print(f"4. Construir aplicación (opcional):")
    print(f"   npm run build")
    print(f"")
    print(f"🌟 ¡Tu aplicación Vader está lista para usar!")

def main():
    """Función principal"""
    if len(sys.argv) != 3:
        print("Uso: python3 generar_app_electron.py <archivo.vdr> <directorio_salida>")
        print("")
        print("Ejemplo:")
        print("  python3 generar_app_electron.py mi_editor.vdr ./mi_editor_app")
        return 1
    
    archivo_vdr = sys.argv[1]
    directorio_salida = sys.argv[2]
    
    print("🌟 GENERADOR DE APLICACIONES ELECTRON VADER")
    print("=" * 50)
    
    if generar_aplicacion_electron(archivo_vdr, directorio_salida):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
