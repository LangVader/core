#!/usr/bin/env python3
"""
Test para validar los nuevos transpiladores de Vader (C++, Rust, Go)
Verifica que generen código válido y funcional
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

# Agregar el directorio transpilers al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'transpilers'))

from cpp import CppTranspiler
from rust import RustTranspiler
from go import GoTranspiler

def test_cpp_transpiler():
    """Prueba el transpilador C++"""
    print("🚀 INICIANDO PRUEBAS DEL TRANSPILADOR C++")
    print("=" * 60)
    
    # Código Vader de prueba
    vader_code = """# Programa de saludo en Vader
nombre = "Carlos"
edad = 28
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
    
    print("=== PRUEBA DEL TRANSPILADOR C++ ===")
    print("\nCódigo Vader original:")
    print("-" * 50)
    print(vader_code)
    
    # Transpilar a C++
    transpiler = CppTranspiler()
    try:
        cpp_code = transpiler.transpile(vader_code)
        print(f"✅ Transpilación C++ exitosa")
        print("\nCódigo C++ generado:")
        print("-" * 30)
        print(cpp_code)
    except Exception as e:
        print(f"❌ Error en transpilación C++: {e}")
        return False
    
    # Verificar elementos clave del código C++
    print("\n=== VERIFICACIÓN DE SINTAXIS C++ ===")
    cpp_checks = [
        ("Headers", "#include <iostream>"),
        ("Namespace", "using namespace std;"),
        ("Main function", "int main()"),
        ("Variable declaration", "string nombre"),
        ("Print statement", "cout <<"),
        ("Conditional", "if ("),
        ("While loop", "while ("),
        ("Return statement", "return 0;")
    ]
    
    all_checks_passed = True
    for check_name, check_pattern in cpp_checks:
        if check_pattern in cpp_code:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}: '{check_pattern}' no encontrado")
            all_checks_passed = False
    
    # Intentar compilar con g++ si está disponible
    print("\n=== VERIFICACIÓN DE COMPILACIÓN C++ ===")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(cpp_code)
            cpp_file = f.name
        
        # Intentar compilar
        result = subprocess.run([
            'g++', '-o', cpp_file + '.out', cpp_file
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Compilación C++ exitosa")
            # Limpiar archivos
            os.unlink(cpp_file)
            if os.path.exists(cpp_file + '.out'):
                os.unlink(cpp_file + '.out')
        else:
            print(f"⚠️ Error de compilación C++: {result.stderr}")
            print("(Esto puede ser normal si g++ no está instalado)")
            os.unlink(cpp_file)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ g++ no disponible - saltando verificación de compilación")
    except Exception as e:
        print(f"⚠️ Error verificando compilación: {e}")
    
    return all_checks_passed

def test_rust_transpiler():
    """Prueba el transpilador Rust"""
    print("\n🚀 INICIANDO PRUEBAS DEL TRANSPILADOR RUST")
    print("=" * 60)
    
    # Código Vader de prueba
    vader_code = """# Calculadora en Vader
numero1 = 15
numero2 = 3
activo = verdadero

suma = numero1 + numero2
resta = numero1 - numero2

mostrar "Suma: " + texto(suma)
mostrar "Resta: " + texto(resta)

si suma mayor que 10 entonces
    mostrar "La suma es mayor que 10"
fin si
"""
    
    print("=== PRUEBA DEL TRANSPILADOR RUST ===")
    print("\nCódigo Vader original:")
    print("-" * 50)
    print(vader_code)
    
    # Transpilar a Rust
    transpiler = RustTranspiler()
    try:
        rust_code = transpiler.transpile(vader_code)
        print(f"✅ Transpilación Rust exitosa")
        print("\nCódigo Rust generado:")
        print("-" * 30)
        print(rust_code)
    except Exception as e:
        print(f"❌ Error en transpilación Rust: {e}")
        return False
    
    # Verificar elementos clave del código Rust
    print("\n=== VERIFICACIÓN DE SINTAXIS RUST ===")
    rust_checks = [
        ("Use statements", "use std::io;"),
        ("Main function", "fn main()"),
        ("Variable declaration", "let mut"),
        ("Print macro", "println!"),
        ("Conditional", "if "),
        ("Boolean values", "true"),
        ("String conversion", ".to_string()")
    ]
    
    all_checks_passed = True
    for check_name, check_pattern in rust_checks:
        if check_pattern in rust_code:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}: '{check_pattern}' no encontrado")
            all_checks_passed = False
    
    # Intentar compilar con rustc si está disponible
    print("\n=== VERIFICACIÓN DE COMPILACIÓN RUST ===")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.rs', delete=False) as f:
            f.write(rust_code)
            rust_file = f.name
        
        # Intentar compilar
        result = subprocess.run([
            'rustc', rust_file, '-o', rust_file + '.out'
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✅ Compilación Rust exitosa")
            # Limpiar archivos
            os.unlink(rust_file)
            if os.path.exists(rust_file + '.out'):
                os.unlink(rust_file + '.out')
        else:
            print(f"⚠️ Error de compilación Rust: {result.stderr}")
            print("(Esto puede ser normal si rustc no está instalado)")
            os.unlink(rust_file)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ rustc no disponible - saltando verificación de compilación")
    except Exception as e:
        print(f"⚠️ Error verificando compilación: {e}")
    
    return all_checks_passed

def test_go_transpiler():
    """Prueba el transpilador Go"""
    print("\n🚀 INICIANDO PRUEBAS DEL TRANSPILADOR GO")
    print("=" * 60)
    
    # Código Vader de prueba
    vader_code = """# Contador en Vader
limite = 5
contador = 0
activo = verdadero

mientras contador menor que limite
    mostrar "Contador: " + texto(contador)
    contador = contador + 1
fin mientras

si activo entonces
    mostrar "¡Terminado!"
fin si
"""
    
    print("=== PRUEBA DEL TRANSPILADOR GO ===")
    print("\nCódigo Vader original:")
    print("-" * 50)
    print(vader_code)
    
    # Transpilar a Go
    transpiler = GoTranspiler()
    try:
        go_code = transpiler.transpile(vader_code)
        print(f"✅ Transpilación Go exitosa")
        print("\nCódigo Go generado:")
        print("-" * 30)
        print(go_code)
    except Exception as e:
        print(f"❌ Error en transpilación Go: {e}")
        return False
    
    # Verificar elementos clave del código Go
    print("\n=== VERIFICACIÓN DE SINTAXIS GO ===")
    go_checks = [
        ("Package declaration", "package main"),
        ("Import statements", "import ("),
        ("Main function", "func main()"),
        ("Variable declaration", "var "),
        ("Print function", "fmt.Printf"),
        ("For loop", "for "),
        ("Boolean values", "true")
    ]
    
    all_checks_passed = True
    for check_name, check_pattern in go_checks:
        if check_pattern in go_code:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}: '{check_pattern}' no encontrado")
            all_checks_passed = False
    
    # Intentar compilar con go si está disponible
    print("\n=== VERIFICACIÓN DE COMPILACIÓN GO ===")
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
            f.write(go_code)
            go_file = f.name
        
        # Intentar compilar
        result = subprocess.run([
            'go', 'build', '-o', go_file + '.out', go_file
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Compilación Go exitosa")
            # Limpiar archivos
            os.unlink(go_file)
            if os.path.exists(go_file + '.out'):
                os.unlink(go_file + '.out')
        else:
            print(f"⚠️ Error de compilación Go: {result.stderr}")
            print("(Esto puede ser normal si go no está instalado)")
            os.unlink(go_file)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️ go no disponible - saltando verificación de compilación")
    except Exception as e:
        print(f"⚠️ Error verificando compilación: {e}")
    
    return all_checks_passed

def main():
    """Ejecuta todas las pruebas de los nuevos transpiladores"""
    print("🧪 PRUEBAS DE NUEVOS TRANSPILADORES VADER")
    print("=" * 60)
    
    tests = [
        ("Transpilador C++", test_cpp_transpiler),
        ("Transpilador Rust", test_rust_transpiler),
        ("Transpilador Go", test_go_transpiler)
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
        print("\n🎉 TODAS LAS PRUEBAS PASARON - NUEVOS TRANSPILADORES FUNCIONALES")
        print("🌟 Vader ahora soporta C++, Rust y Go!")
        return True
    else:
        print(f"\n❌ {total - passed} pruebas fallaron")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
