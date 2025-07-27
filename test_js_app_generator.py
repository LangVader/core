#!/usr/bin/env python3
"""
Test script para validar el generador de aplicaciones JavaScript
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Añadir el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app_generator import VaderAppGenerator

def test_js_web_app():
    """Prueba la generación de aplicación web JavaScript"""
    
    # Código Vader de prueba
    vader_code = """
# Programa de saludo en Vader
nombre = "María"
edad = 30
activo = verdadero

mostrar "¡Hola! Mi nombre es " + nombre
mostrar "Tengo " + texto(edad) + " años"

si edad mayor que 18 entonces
    mostrar "Soy mayor de edad"
sino
    mostrar "Soy menor de edad"
fin si

contador = 1
mientras contador menor que 4
    mostrar "Contando: " + texto(contador)
    contador = contador + 1
fin mientras

repetir 3 veces
    mostrar "Repetición número: " + texto(i + 1)
fin repetir
"""
    
    print("=== PRUEBA DEL GENERADOR DE APLICACIONES JAVASCRIPT ===")
    print("\nCódigo Vader original:")
    print("-" * 50)
    print(vader_code.strip())
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Generar aplicación JavaScript
            generator = VaderAppGenerator()
            app_dir = generator.generate_complete_app(
                vader_code, 
                temp_dir, 
                "MiAppVader", 
                target_language="javascript"
            )
            
            print(f"\n✅ APLICACIÓN GENERADA EN: {app_dir}")
            
            # Verificar estructura de archivos
            expected_files = [
                'index.html',
                'js/app.js',
                'css/style.css',
                'package.json',
                'README.md'
            ]
            
            print("\n=== VERIFICACIÓN DE ARCHIVOS ===")
            all_files_exist = True
            
            for file_path in expected_files:
                full_path = app_dir / file_path
                exists = full_path.exists()
                status = "✅" if exists else "❌"
                print(f"{status} {file_path}")
                if not exists:
                    all_files_exist = False
            
            if all_files_exist:
                print("\n✅ TODOS LOS ARCHIVOS GENERADOS CORRECTAMENTE")
                
                # Mostrar contenido del HTML generado
                print("\n=== CONTENIDO DEL HTML ===")
                with open(app_dir / 'index.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    print("HTML generado correctamente ✅")
                    print(f"Tamaño: {len(html_content)} caracteres")
                
                # Mostrar contenido del JavaScript generado
                print("\n=== CONTENIDO DEL JAVASCRIPT ===")
                with open(app_dir / 'js' / 'app.js', 'r', encoding='utf-8') as f:
                    js_content = f.read()
                    print("JavaScript generado correctamente ✅")
                    print(f"Tamaño: {len(js_content)} caracteres")
                
                # Verificar que el código Vader transpilado esté incluido
                if "console.log" in js_content and "let nombre" in js_content:
                    print("✅ Código Vader transpilado incluido correctamente")
                else:
                    print("❌ Código Vader transpilado no encontrado")
                
                # Mostrar contenido del package.json
                print("\n=== PACKAGE.JSON ===")
                with open(app_dir / 'package.json', 'r', encoding='utf-8') as f:
                    package_content = f.read()
                    print("package.json generado correctamente ✅")
                
                return True
            else:
                print("\n❌ FALTAN ARCHIVOS EN LA APLICACIÓN GENERADA")
                return False
                
        except Exception as e:
            print(f"\n❌ ERROR GENERANDO APLICACIÓN: {e}")
            return False

def test_js_calculator():
    """Prueba la generación de calculadora JavaScript"""
    
    # Código Vader que indica calculadora
    vader_code = """
# Calculadora simple en Vader
resultado = 0
numero1 = 10
numero2 = 5

# Operaciones básicas
suma = numero1 + numero2
resta = numero1 - numero2
multiplicacion = numero1 * numero2
division = numero1 / numero2

mostrar "Suma: " + texto(suma)
mostrar "Resta: " + texto(resta)
mostrar "Multiplicación: " + texto(multiplicacion)
mostrar "División: " + texto(division)
"""
    
    print("\n=== PRUEBA DE CALCULADORA JAVASCRIPT ===")
    print("\nCódigo Vader para calculadora:")
    print("-" * 50)
    print(vader_code.strip())
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Generar calculadora JavaScript
            generator = VaderAppGenerator()
            app_dir = generator.generate_js_web_calculator(temp_dir, "CalculadoraJS")
            
            print(f"\n✅ CALCULADORA GENERADA EN: {app_dir}")
            
            # Verificar estructura de archivos de calculadora
            expected_files = [
                'index.html',
                'js/calculator.js',
                'css/calculator.css',
                'package.json',
                'README.md'
            ]
            
            print("\n=== VERIFICACIÓN DE ARCHIVOS DE CALCULADORA ===")
            all_files_exist = True
            
            for file_path in expected_files:
                full_path = app_dir / file_path
                exists = full_path.exists()
                status = "✅" if exists else "❌"
                print(f"{status} {file_path}")
                if not exists:
                    all_files_exist = False
            
            if all_files_exist:
                print("\n✅ CALCULADORA GENERADA CORRECTAMENTE")
                
                # Verificar funcionalidad JavaScript de calculadora
                with open(app_dir / 'js' / 'calculator.js', 'r', encoding='utf-8') as f:
                    calc_js = f.read()
                
                # Verificar funciones clave
                functions_check = [
                    ("función numero()", "function numero(" in calc_js),
                    ("función operacion()", "function operacion(" in calc_js),
                    ("función calcular()", "function calcular(" in calc_js),
                    ("función limpiar()", "function limpiar(" in calc_js),
                    ("soporte teclado", "addEventListener('keydown'" in calc_js)
                ]
                
                print("\n=== VERIFICACIÓN DE FUNCIONES ===")
                for func_name, exists in functions_check:
                    status = "✅" if exists else "❌"
                    print(f"{status} {func_name}")
                
                return all(exists for _, exists in functions_check)
            else:
                print("\n❌ FALTAN ARCHIVOS EN LA CALCULADORA")
                return False
                
        except Exception as e:
            print(f"\n❌ ERROR GENERANDO CALCULADORA: {e}")
            return False

def main():
    """Función principal de pruebas"""
    print("🚀 INICIANDO PRUEBAS DEL GENERADOR DE APLICACIONES JAVASCRIPT")
    print("=" * 70)
    
    # Ejecutar pruebas
    test1_passed = test_js_web_app()
    test2_passed = test_js_calculator()
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 70)
    
    tests = [
        ("Aplicación Web JavaScript", test1_passed),
        ("Calculadora JavaScript", test2_passed)
    ]
    
    passed_tests = sum(1 for _, passed in tests if passed)
    total_tests = len(tests)
    
    for test_name, passed in tests:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{status} {test_name}")
    
    print(f"\nResultado: {passed_tests}/{total_tests} pruebas pasaron")
    
    if passed_tests == total_tests:
        print("\n🎉 TODAS LAS PRUEBAS PASARON - GENERADOR JAVASCRIPT FUNCIONAL")
        print("🌟 Vader puede generar aplicaciones web JavaScript completas!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} PRUEBAS FALLARON")
        print("🔧 Revisar el generador de aplicaciones JavaScript")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
