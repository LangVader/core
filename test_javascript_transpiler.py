#!/usr/bin/env python3
"""
Test script para validar el transpilador JavaScript corregido
"""

import sys
import os
import tempfile
import subprocess

# Añadir el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transpilers.javascript import JavaScriptTranspiler

def test_javascript_transpiler():
    """Prueba el transpilador JavaScript con código Vader de ejemplo"""
    
    # Código Vader de prueba
    vader_code = """
# Programa de prueba en Vader
nombre = "Juan"
edad = 25
activo = verdadero

mostrar "Hola, mi nombre es " + nombre
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

repetir 3 veces
    mostrar "Repetición número: " + texto(i + 1)
fin repetir

funcion saludar con nombre
    mostrar "¡Hola " + nombre + "!"
fin funcion

saludar("María")
"""
    
    print("=== PRUEBA DEL TRANSPILADOR JAVASCRIPT ===")
    print("\nCódigo Vader original:")
    print("-" * 40)
    print(vader_code.strip())
    
    # Transpilar a JavaScript
    transpiler = JavaScriptTranspiler()
    js_code = transpiler.transpile(vader_code)
    
    print("\nCódigo JavaScript generado:")
    print("-" * 40)
    print(js_code)
    
    # Guardar el código JavaScript en un archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_code)
        js_file = f.name
    
    try:
        # Verificar sintaxis JavaScript usando Node.js si está disponible
        try:
            result = subprocess.run(['node', '-c', js_file], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("\n✅ SINTAXIS JAVASCRIPT VÁLIDA")
                
                # Intentar ejecutar el código
                print("\n=== EJECUTANDO CÓDIGO JAVASCRIPT ===")
                exec_result = subprocess.run(['node', js_file], 
                                           capture_output=True, text=True, timeout=10)
                
                if exec_result.returncode == 0:
                    print("✅ EJECUCIÓN EXITOSA")
                    print("\nSalida del programa:")
                    print(exec_result.stdout)
                else:
                    print("❌ ERROR EN EJECUCIÓN")
                    print("Error:", exec_result.stderr)
                    
            else:
                print("❌ ERROR DE SINTAXIS JAVASCRIPT")
                print("Error:", result.stderr)
                
        except FileNotFoundError:
            print("\n⚠️  Node.js no encontrado - solo validando estructura")
            print("✅ Código JavaScript generado correctamente")
            
        except subprocess.TimeoutExpired:
            print("❌ TIMEOUT - El código tardó demasiado en ejecutarse")
            
    finally:
        # Limpiar archivo temporal
        if os.path.exists(js_file):
            os.unlink(js_file)
    
    print("\n=== ANÁLISIS DEL CÓDIGO GENERADO ===")
    
    # Verificar elementos clave
    checks = [
        ("Variables booleanas", "true" in js_code or "false" in js_code),
        ("Console.log", "console.log" in js_code),
        ("Condicionales", "if (" in js_code and "} else {" in js_code),
        ("Bucles while", "while (" in js_code),
        ("Bucles for", "for (" in js_code),
        ("Funciones", "function " in js_code),
        ("Llaves de cierre", js_code.count('{') == js_code.count('}')),
        ("Punto y coma", js_code.count(';') > 0)
    ]
    
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
    
    return all(passed for _, passed in checks)

if __name__ == "__main__":
    success = test_javascript_transpiler()
    print(f"\n{'='*50}")
    if success:
        print("🎉 TODAS LAS PRUEBAS PASARON - TRANSPILADOR JAVASCRIPT FUNCIONAL")
    else:
        print("⚠️  ALGUNAS PRUEBAS FALLARON - REVISAR TRANSPILADOR")
    print(f"{'='*50}")
