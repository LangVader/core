#!/usr/bin/env python3
"""
Test del transpilador Python corregido para Vader
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transpilers.python import transpile_to_python

# Código de prueba en Vader
vader_code = '''# Mi primer programa en Vader
mostrar "¡Hola Mundo desde Vader!"
mostrar "Vader es LA PROGRAMACIÓN universal"

# Variables básicas
nombre = "Programador"
edad = 25
activo = verdadero

mostrar "Hola " + nombre
mostrar "Tienes " + texto(edad) + " años"

# Condicional simple
si edad >= 18 entonces
    mostrar "Eres mayor de edad"
sino
    mostrar "Eres menor de edad"
fin si

# Lista simple
lenguajes = ["Python", "JavaScript", "Vader"]
mostrar "Lenguajes disponibles:"
para cada lenguaje en lenguajes
    mostrar "- " + lenguaje
fin'''

print("=== CÓDIGO VADER ORIGINAL ===")
print(vader_code)
print("\n=== CÓDIGO PYTHON TRANSPILADO ===")

try:
    python_code = transpile_to_python(vader_code)
    print(python_code)
    
    print("\n=== VALIDANDO SINTAXIS PYTHON ===")
    try:
        compile(python_code, '<string>', 'exec')
        print("✅ Sintaxis Python válida!")
        
        print("\n=== EJECUTANDO CÓDIGO ===")
        exec(python_code)
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis Python: {e}")
        print(f"Línea {e.lineno}: {e.text}")
    except Exception as e:
        print(f"❌ Error de ejecución: {e}")
        
except Exception as e:
    print(f"❌ Error en transpilación: {e}")
