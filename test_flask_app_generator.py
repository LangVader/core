#!/usr/bin/env python3
"""
Test para validar el generador de aplicaciones Flask de Vader
Verifica que se generen aplicaciones Flask funcionales desde código Vader
"""

import os
import sys
import tempfile
import shutil
import subprocess
import json
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app_generator import VaderAppGenerator

def test_flask_app_generation():
    """Prueba la generación de aplicación Flask desde código Vader"""
    print("🚀 INICIANDO PRUEBAS DEL GENERADOR FLASK")
    print("=" * 60)
    
    # Código Vader de prueba
    vader_code = """# Aplicación de saludo en Vader
nombre = "María"
edad = 30
activo = verdadero

mostrar "¡Hola desde Flask! Soy " + nombre
mostrar "Tengo " + texto(edad) + " años"

si edad mayor que 18 entonces
    mostrar "Soy mayor de edad"
sino
    mostrar "Soy menor de edad"
fin si

contador = 1
mientras contador menor que 3
    mostrar "Contador: " + texto(contador)
    contador = contador + 1
fin mientras
"""
    
    print("=== PRUEBA DEL GENERADOR FLASK ===")
    print("\nCódigo Vader original:")
    print("-" * 50)
    print(vader_code)
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        app_name = "MiAppFlask"
        output_dir = temp_dir
        
        print(f"🚀 Generando aplicación Flask: {app_name}")
        print(f"📁 Directorio: {output_dir}")
        
        # Generar aplicación Flask
        generator = VaderAppGenerator()
        try:
            result = generator.generate_flask_app(vader_code, output_dir, app_name)
            print(f"✅ Aplicación Flask generada: {result}")
        except Exception as e:
            print(f"❌ Error generando Flask app: {e}")
            return False
        
        # El método devuelve el directorio real donde se crearon los archivos
        actual_output_dir = str(result)
        
        # Verificar estructura de archivos
        print("\n=== VERIFICACIÓN DE ESTRUCTURA ===")
        expected_files = [
            "app.py",
            "templates/index.html",
            "static/style.css",
            "requirements.txt",
            "README.md"
        ]
        
        all_files_exist = True
        for file_path in expected_files:
            full_path = os.path.join(actual_output_dir, file_path)
            if os.path.exists(full_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path}")
                all_files_exist = False
        
        if not all_files_exist:
            print("❌ Faltan archivos en la estructura")
            return False
        
        # Verificar contenido de archivos clave
        print("\n=== VERIFICACIÓN DE CONTENIDO ===")
        
        # Verificar app.py
        app_py_path = os.path.join(actual_output_dir, "app.py")
        with open(app_py_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        app_checks = [
            ("Flask import", "from flask import Flask"),
            ("App creation", "app = Flask(__name__)"),
            ("Route definition", "@app.route"),
            ("Transpiled code", "María"),
            ("Python syntax", "print("),
            ("Main block", "if __name__ == '__main__':")
        ]
        
        for check_name, check_pattern in app_checks:
            if check_pattern in app_content:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}: '{check_pattern}' no encontrado")
                return False
        
        # Verificar index.html
        html_path = os.path.join(actual_output_dir, "templates", "index.html")
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        html_checks = [
            ("HTML structure", "<!DOCTYPE html>"),
            ("Title", "<title>"),
            ("CSS link", "style.css"),
            ("Container div", "container"),
            ("Execute button", "button")
        ]
        
        for check_name, check_pattern in html_checks:
            if check_pattern in html_content:
                print(f"✅ HTML {check_name}")
            else:
                print(f"❌ HTML {check_name}: '{check_pattern}' no encontrado")
                return False
        
        # Verificar requirements.txt
        req_path = os.path.join(actual_output_dir, "requirements.txt")
        with open(req_path, 'r', encoding='utf-8') as f:
            req_content = f.read()
        
        if "Flask" in req_content:
            print("✅ Flask en requirements.txt")
        else:
            print("❌ Flask no encontrado en requirements.txt")
            return False
        
        # Verificar sintaxis Python del archivo generado
        print("\n=== VERIFICACIÓN DE SINTAXIS PYTHON ===")
        try:
            result = subprocess.run([
                sys.executable, "-m", "py_compile", app_py_path
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Sintaxis Python válida")
            else:
                print(f"❌ Error de sintaxis Python: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ Timeout verificando sintaxis Python")
            return False
        except Exception as e:
            print(f"❌ Error verificando sintaxis: {e}")
            return False
        
        print(f"\n✅ APLICACIÓN FLASK GENERADA EN: {actual_output_dir}")
        return True

def test_flask_calculator_generation():
    """Prueba la generación de calculadora Flask desde código Vader"""
    print("\n=== PRUEBA DE CALCULADORA FLASK ===")
    
    # Código Vader para calculadora
    vader_code = """# Calculadora en Vader
numero1 = 10
numero2 = 5

suma = numero1 + numero2
resta = numero1 - numero2
multiplicacion = numero1 * numero2
division = numero1 / numero2

mostrar "Suma: " + texto(suma)
mostrar "Resta: " + texto(resta)
mostrar "Multiplicación: " + texto(multiplicacion)
mostrar "División: " + texto(division)
"""
    
    print("Código Vader calculadora:")
    print("-" * 30)
    print(vader_code)
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        app_name = "CalculadoraFlask"
        output_dir = temp_dir
        
        print(f"🚀 Generando calculadora Flask: {app_name}")
        
        # Generar aplicación Flask
        generator = VaderAppGenerator()
        try:
            result = generator.generate_flask_app(vader_code, output_dir, app_name)
            print(f"✅ Calculadora Flask generada: {result}")
        except Exception as e:
            print(f"❌ Error generando calculadora Flask: {e}")
            return False
        
        # El método devuelve el directorio real donde se crearon los archivos
        actual_output_dir = str(result)
        
        # Verificar que contiene operaciones matemáticas
        app_py_path = os.path.join(actual_output_dir, "app.py")
        with open(app_py_path, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        math_checks = [
            ("Suma", "+"),
            ("Resta", "-"),
            ("Multiplicación", "*"),
            ("División", "/"),
            ("Variables numéricas", "numero1"),
            ("Print statements", "print(")
        ]
        
        for check_name, check_pattern in math_checks:
            if check_pattern in app_content:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}: '{check_pattern}' no encontrado")
                return False
        
        return True

def main():
    """Ejecuta todas las pruebas del generador Flask"""
    print("🧪 PRUEBAS DEL GENERADOR DE APLICACIONES FLASK VADER")
    print("=" * 60)
    
    tests = [
        ("Generación Flask App", test_flask_app_generation),
        ("Generación Calculadora Flask", test_flask_calculator_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"✅ PASÓ {test_name}")
                passed += 1
            else:
                print(f"❌ FALLÓ {test_name}")
        except Exception as e:
            print(f"❌ ERROR en {test_name}: {e}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASÓ" if i < passed else "❌ FALLÓ"
        print(f"{status} {test_name}")
    
    print(f"\nResultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("\n🎉 TODAS LAS PRUEBAS PASARON - GENERADOR FLASK FUNCIONAL")
        print("🌟 Vader puede generar aplicaciones Flask completas!")
        return True
    else:
        print(f"\n❌ {total - passed} pruebas fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
