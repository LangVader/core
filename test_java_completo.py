#!/usr/bin/env python3
"""
Test del Transpilador Java COMPLETO para Vader
Valida todas las características avanzadas implementadas
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'transpilers'))

from java import JavaTranspiler

def test_java_completo():
    """Test completo del transpilador Java con todas las características"""
    
    # Código Vader con todas las características avanzadas
    vader_code = '''
# Test completo del transpilador Java
mostrar "=== Test Transpilador Java COMPLETO ==="

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
crear array numeros de tamaño 5

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
    
    funcion presentarse que devuelve texto:
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
    
    print("🧪 Iniciando test del transpilador Java COMPLETO...")
    
    # Crear transpilador
    transpiler = JavaTranspiler()
    
    # Transpilar código
    java_code = transpiler.transpile(vader_code)
    
    print("✅ Transpilación completada!")
    print("\n" + "="*60)
    print("CÓDIGO JAVA GENERADO:")
    print("="*60)
    print(java_code)
    print("="*60)
    
    # Validaciones
    validaciones = [
        ("Imports correctos", "import java.util.Scanner;" in java_code),
        ("Clase principal", "public class VaderProgram" in java_code),
        ("Variables tipadas", "int edad" in java_code),
        ("Listas", "List<String> amigos = new ArrayList<>" in java_code),
        ("Funciones con tipos", "public static String saludar(String persona)" in java_code),
        ("Clases personalizadas", "public static class Persona" in java_code),
        ("Constructores", "public Persona(String nombre, int edad)" in java_code),
        ("Try-catch", "try {" in java_code and "} catch (Exception e)" in java_code),
        ("Operaciones matemáticas", "Math.sqrt" in java_code and "Math.pow" in java_code),
        ("Condicionales", "if (edad > 18)" in java_code),
        ("Bucles", "for (int i = 0; i < 3; i++)" in java_code)
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
        print("🎉 ¡TRANSPILADOR JAVA COMPLETO Y FUNCIONAL!")
        return True
    else:
        print("⚠️ El transpilador necesita mejoras")
        return False

if __name__ == "__main__":
    test_java_completo()
