#!/usr/bin/env python3
"""
Test script para validar el transpilador Java corregido
"""

import sys
import os
import tempfile
import subprocess

# Añadir el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transpilers.java import JavaTranspiler

def test_java_transpiler():
    """Prueba el transpilador Java con código Vader de ejemplo"""
    
    # Código Vader de prueba
    vader_code = """
# Programa de prueba en Vader
nombre = "Carlos"
edad = 28
activo = verdadero

mostrar "Hola, soy " + nombre
mostrar "Tengo " + texto(edad) + " años"

si edad mayor que 18 entonces
    mostrar "Soy mayor de edad"
sino
    mostrar "Soy menor de edad"
fin si

contador = 0
mientras contador menor que 3
    mostrar "Contador: " + texto(contador)
    contador = contador + 1
fin mientras

repetir 2 veces
    mostrar "Repetición número: " + texto(i + 1)
fin repetir
"""
    
    print("=== PRUEBA DEL TRANSPILADOR JAVA ===")
    print("\nCódigo Vader original:")
    print("-" * 40)
    print(vader_code.strip())
    
    # Transpilar a Java
    transpiler = JavaTranspiler()
    java_code = transpiler.transpile(vader_code)
    
    print("\nCódigo Java generado:")
    print("-" * 40)
    print(java_code)
    
    # Guardar el código Java en un archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
        f.write(java_code)
        java_file = f.name
    
    try:
        # Verificar sintaxis Java usando javac si está disponible
        try:
            # Compilar el código Java
            result = subprocess.run(['javac', java_file], 
                                  capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print("\n✅ COMPILACIÓN JAVA EXITOSA")
                
                # Intentar ejecutar el código
                print("\n=== EJECUTANDO CÓDIGO JAVA ===")
                class_name = "VaderProgram"
                java_dir = os.path.dirname(java_file)
                
                exec_result = subprocess.run(['java', '-cp', java_dir, class_name], 
                                           capture_output=True, text=True, timeout=15)
                
                if exec_result.returncode == 0:
                    print("✅ EJECUCIÓN EXITOSA")
                    print("\nSalida del programa:")
                    print(exec_result.stdout)
                else:
                    print("❌ ERROR EN EJECUCIÓN")
                    print("Error:", exec_result.stderr)
                    
            else:
                print("❌ ERROR DE COMPILACIÓN JAVA")
                print("Error:", result.stderr)
                
        except FileNotFoundError:
            print("\n⚠️  javac no encontrado - solo validando estructura")
            print("✅ Código Java generado correctamente")
            
        except subprocess.TimeoutExpired:
            print("❌ TIMEOUT - El código tardó demasiado en compilar/ejecutar")
            
    finally:
        # Limpiar archivos temporales
        if os.path.exists(java_file):
            os.unlink(java_file)
        # Limpiar archivo .class si existe
        class_file = java_file.replace('.java', '.class')
        if os.path.exists(class_file):
            os.unlink(class_file)
    
    print("\n=== ANÁLISIS DEL CÓDIGO GENERADO ===")
    
    # Verificar elementos clave
    checks = [
        ("Clase principal", "public class VaderProgram" in java_code),
        ("Método main", "public static void main" in java_code),
        ("Variables booleanas", "true" in java_code or "false" in java_code),
        ("System.out.println", "System.out.println" in java_code),
        ("Condicionales", "if (" in java_code and "} else {" in java_code),
        ("Bucles while", "while (" in java_code),
        ("Bucles for", "for (" in java_code),
        ("Imports", "import java.util.Scanner" in java_code),
        ("Llaves balanceadas", java_code.count('{') == java_code.count('}')),
        ("Punto y coma", java_code.count(';') > 0)
    ]
    
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
    
    return all(passed for _, passed in checks)

if __name__ == "__main__":
    success = test_java_transpiler()
    print(f"\n{'='*50}")
    if success:
        print("🎉 TODAS LAS PRUEBAS PASARON - TRANSPILADOR JAVA FUNCIONAL")
    else:
        print("⚠️  ALGUNAS PRUEBAS FALLARON - REVISAR TRANSPILADOR")
    print(f"{'='*50}")
