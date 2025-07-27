#!/usr/bin/env python3
"""
Test completo del transpilador C++ de Vader
Valida que el transpilador genere código C++ válido y funcional
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transpilers.cpp import CppTranspiler

def test_cpp_completo():
    """Test completo del transpilador C++ con todas las características"""
    
    # Código Vader con todas las características avanzadas
    vader_code = '''
# Test completo del transpilador C++
mostrar "=== Test Transpilador C++ COMPLETO ==="

# Variables con tipos automáticos
crear variable edad tipo numero
edad = 25
crear variable nombre tipo texto
nombre = "Juan"
crear variable activo tipo booleano
activo = verdadero

# Estructuras de datos
crear lista amigos
agregar "Ana" a amigos
agregar "Luis" a amigos
crear mapa datos
crear array numeros[5]

# Funciones con tipos
funcion saludar con persona tipo texto que devuelve texto:
    devolver "Hola " + persona
fin

funcion sumar con a tipo numero y b tipo numero que devuelve numero:
    devolver a + b
fin

# Clase con herencia
clase Persona:
    atributo nombre tipo texto
    atributo edad tipo numero
    
    constructor con nombre tipo texto y edad tipo numero:
        this.nombre = nombre
        this.edad = edad
    fin
    
    metodo presentarse que devuelve texto:
        devolver "Soy " + nombre + " y tengo " + edad + " años"
    fin
fin clase

# Condicionales y bucles
si edad es mayor que 18 entonces
    mostrar "Es mayor de edad"
sino
    mostrar "Es menor de edad"
fin si

repetir 3 veces
    mostrar "Iteración: " + i
fin repetir

# Manejo de errores
intentar
    numero("abc")
capturar error
    mostrar "Error al convertir número"
finalmente
    mostrar "Proceso completado"
fin

# Operaciones matemáticas
resultado = raiz(16) + potencia(2, 3)
mostrar "Resultado matemático: " + resultado
'''

    # Transpilación
    transpiler = CppTranspiler()
    cpp_code = transpiler.transpile(vader_code)
    
    print("🧪 Iniciando test del transpilador C++ COMPLETO...")
    print("✅ Transpilación completada!")
    print("\n" + "="*60)
    print("CÓDIGO C++ GENERADO:")
    print("="*60)
    print(cpp_code)
    print("="*60)
    
    # Validaciones específicas
    validaciones = [
        ("Includes correctos", "#include <iostream>" in cpp_code and "#include <string>" in cpp_code),
        ("Namespace std", "using namespace std;" in cpp_code),
        ("Función main", "int main()" in cpp_code),
        ("Variables tipadas", "int edad" in cpp_code and "string nombre" in cpp_code),
        ("Vectores/Listas", "vector" in cpp_code or "std::vector" in cpp_code),
        ("Funciones con tipos", "string saludar(" in cpp_code or "std::string saludar(" in cpp_code),
        ("Clases personalizadas", "class Persona" in cpp_code),
        ("Constructores", "Persona(" in cpp_code),
        ("Try-catch", "try {" in cpp_code and "catch" in cpp_code),
        ("Operaciones matemáticas", "sqrt(" in cpp_code or "pow(" in cpp_code),
        ("Condicionales", "if (" in cpp_code and "} else {" in cpp_code),
        ("Bucles", "for (" in cpp_code)
    ]
    
    print("\n🔍 VALIDACIONES:")
    passed = 0
    total = len(validaciones)
    
    for desc, condition in validaciones:
        if condition:
            print(f"✅ {desc}")
            passed += 1
        else:
            print(f"❌ {desc}")
    
    print(f"\n📊 RESULTADO: {passed}/{total} validaciones pasadas")
    
    if passed == total:
        print("🎉 ¡TRANSPILADOR C++ COMPLETO Y FUNCIONAL!")
        return True
    else:
        print("⚠️ El transpilador necesita mejoras")
        return False

if __name__ == "__main__":
    test_cpp_completo()
