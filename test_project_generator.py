#!/usr/bin/env python3
"""
Test script para validar el generador de proyectos completos
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Añadir el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.project_generator import VaderProjectGenerator

def test_complete_project_generation():
    """Prueba la generación de proyecto completo multi-lenguaje"""
    
    # Código Vader de prueba
    vader_code = """
# Aplicación de saludo en Vader
nombre = "Ana"
edad = 25
activo = verdadero

mostrar "¡Hola! Soy " + nombre
mostrar "Tengo " + texto(edad) + " años"

si edad mayor que 18 entonces
    mostrar "Soy mayor de edad"
sino
    mostrar "Soy menor de edad"
fin si

contador = 1
mientras contador menor que 4
    mostrar "Iteración: " + texto(contador)
    contador = contador + 1
fin mientras
"""
    
    print("=== PRUEBA DEL GENERADOR DE PROYECTOS COMPLETOS ===")
    print("\nCódigo Vader original:")
    print("-" * 50)
    print(vader_code.strip())
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Generar proyecto completo
            generator = VaderProjectGenerator()
            project_dir = generator.generate_complete_project(
                vader_code, 
                "MiProyectoVader", 
                temp_dir,
                target_languages=['python', 'javascript', 'java'],
                project_type='web_app'
            )
            
            print(f"\n✅ PROYECTO GENERADO EN: {project_dir}")
            
            # Verificar estructura de archivos
            expected_files = [
                'README.md',
                'requirements.txt',
                'package.json',
                'pom.xml',
                'src/python/main.py',
                'src/javascript/main.js',
                'src/java/VaderProgram.java',
                'tests/python/test_main.py',
                'tests/javascript/main.test.js',
                'tests/java/VaderTest.java',
                'docs/development.md'
            ]
            
            print("\n=== VERIFICACIÓN DE ESTRUCTURA ===")
            all_files_exist = True
            
            for file_path in expected_files:
                full_path = project_dir / file_path
                exists = full_path.exists()
                status = "✅" if exists else "❌"
                print(f"{status} {file_path}")
                if not exists:
                    all_files_exist = False
            
            # Verificar contenido de archivos clave
            if all_files_exist:
                print("\n=== VERIFICACIÓN DE CONTENIDO ===")
                
                # Verificar README
                readme_path = project_dir / 'README.md'
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                readme_checks = [
                    ("Título del proyecto", "MiProyectoVader" in readme_content),
                    ("Código Vader incluido", "nombre = \"Ana\"" in readme_content),
                    ("Instrucciones Python", "pip install" in readme_content),
                    ("Instrucciones JavaScript", "npm install" in readme_content),
                    ("Instrucciones Java", "mvn compile" in readme_content),
                    ("Estructura del proyecto", "src/" in readme_content)
                ]
                
                for check_name, passed in readme_checks:
                    status = "✅" if passed else "❌"
                    print(f"{status} README: {check_name}")
                
                # Verificar código Python generado
                python_path = project_dir / 'src' / 'python' / 'main.py'
                with open(python_path, 'r', encoding='utf-8') as f:
                    python_content = f.read()
                
                python_checks = [
                    ("Header de Vader", "Código generado automáticamente por Vader" in python_content),
                    ("Variables convertidas", "nombre = \"Ana\"" in python_content),
                    ("Print statements", "print(" in python_content),
                    ("Condicionales", "if " in python_content and "else:" in python_content)
                ]
                
                for check_name, passed in python_checks:
                    status = "✅" if passed else "❌"
                    print(f"{status} Python: {check_name}")
                
                # Verificar configuración de dependencias
                config_checks = [
                    ("requirements.txt existe", (project_dir / 'requirements.txt').exists()),
                    ("package.json existe", (project_dir / 'package.json').exists()),
                    ("pom.xml existe", (project_dir / 'pom.xml').exists())
                ]
                
                for check_name, passed in config_checks:
                    status = "✅" if passed else "❌"
                    print(f"{status} Config: {check_name}")
                
                return all_files_exist and all(passed for _, passed in readme_checks + python_checks + config_checks)
            else:
                print("\n❌ FALTAN ARCHIVOS EN EL PROYECTO GENERADO")
                return False
                
        except Exception as e:
            print(f"\n❌ ERROR GENERANDO PROYECTO: {e}")
            return False

def test_single_language_project():
    """Prueba generación de proyecto con un solo lenguaje"""
    
    vader_code = """
# Calculadora simple
numero1 = 10
numero2 = 5
resultado = numero1 + numero2
mostrar "El resultado es: " + texto(resultado)
"""
    
    print("\n=== PRUEBA DE PROYECTO PYTHON ÚNICO ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            generator = VaderProjectGenerator()
            project_dir = generator.generate_complete_project(
                vader_code, 
                "CalculadoraVader", 
                temp_dir,
                target_languages=['python'],
                project_type='console'
            )
            
            # Verificar que solo se generaron archivos Python
            python_file = project_dir / 'src' / 'python' / 'main.py'
            js_file = project_dir / 'src' / 'javascript' / 'main.js'
            java_file = project_dir / 'src' / 'java' / 'VaderProgram.java'
            
            checks = [
                ("Archivo Python generado", python_file.exists()),
                ("Archivo JavaScript NO generado", not js_file.exists()),
                ("Archivo Java NO generado", not java_file.exists()),
                ("requirements.txt generado", (project_dir / 'requirements.txt').exists()),
                ("package.json NO generado", not (project_dir / 'package.json').exists())
            ]
            
            print("\n=== VERIFICACIÓN LENGUAJE ÚNICO ===")
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"{status} {check_name}")
            
            return all(passed for _, passed in checks)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL GENERADOR DE PROYECTOS")
    print("=" * 60)
    
    # Ejecutar pruebas
    test1_passed = test_complete_project_generation()
    test2_passed = test_single_language_project()
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    tests = [
        ("Proyecto Multi-lenguaje", test1_passed),
        ("Proyecto Lenguaje Único", test2_passed)
    ]
    
    passed_tests = sum(1 for _, passed in tests if passed)
    total_tests = len(tests)
    
    for test_name, passed in tests:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{status} {test_name}")
    
    print(f"\nResultado: {passed_tests}/{total_tests} pruebas pasaron")
    
    if passed_tests == total_tests:
        print("\n🎉 TODAS LAS PRUEBAS PASARON - GENERADOR DE PROYECTOS FUNCIONAL")
        print("🌟 Vader puede generar proyectos completos multi-lenguaje!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} PRUEBAS FALLARON")
        print("🔧 Revisar el generador de proyectos")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
