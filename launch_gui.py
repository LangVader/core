#!/usr/bin/env python3
"""
VADER GUI LAUNCHER
Lanza la interfaz gráfica moderna, oscura y minimalista de Vader
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Verificar dependencias necesarias"""
    try:
        import tkinter
        print("✅ Tkinter disponible")
    except ImportError:
        print("❌ Error: Tkinter no está instalado")
        print("En Ubuntu/Debian: sudo apt-get install python3-tk")
        print("En macOS: Tkinter viene incluido con Python")
        return False
        
    try:
        from gui.main_app import VaderGUI
        print("✅ Módulos GUI de Vader disponibles")
    except ImportError as e:
        print(f"❌ Error: No se pudo importar GUI de Vader: {e}")
        return False
        
    return True

def main():
    """Función principal"""
    print("🚀 VADER GUI - Interfaz Gráfica Moderna")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ No se puede iniciar la GUI. Verifica las dependencias.")
        return 1
    
    try:
        # Importar y lanzar GUI
        from gui.main_app import VaderGUI
        
        print("✅ Iniciando interfaz gráfica...")
        print("🎨 Tema: Oscuro y minimalista con negro predominante")
        print("⚡ Características: Editor, IA integrada, Vista previa")
        print("\n🔥 ¡VADER - EL LENGUAJE SUPREMO UNIVERSAL!")
        
        # Crear y ejecutar aplicación
        app = VaderGUI()
        app.run()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Aplicación cerrada por el usuario")
        return 0
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
