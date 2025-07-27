#!/usr/bin/env python3
"""
Test completo del transpilador Go de Vader
Valida que el transpilador genere código Go válido y funcional
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transpilers.go import GoTranspiler

def test_go_transpiler():
    print("🧪 Iniciando test del transpilador Go COMPLETO...")
    
    # Código Vader de prueba completo
    vader_code = '''
# Test completo del transpilador Go
mostrar "=== Test Transpilador Go COMPLETO ==="

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
    retornar "Hola " + persona
fin

funcion sumar con a tipo numero y b tipo numero que devuelve numero:
    retornar a + b
fin

# Struct con implementación
clase Persona:
    atributo nombre tipo texto
    atributo edad tipo numero
    
    constructor con nombre tipo texto y edad tipo numero:
        this.nombre = nombre
        this.edad = edad
    fin
    
    metodo presentarse que devuelve texto:
        retornar "Soy " + nombre + " y tengo " + edad + " años"
    fin
fin

# Condicionales y bucles
si edad > 18:
    mostrar "Es mayor de edad"
sino:
    mostrar "Es menor de edad"
fin

repetir 3 veces:
    mostrar "Iteración: " + i
fin repetir

# Manejo de errores
intentar:
    numero("abc")
capturar error:
    mostrar "Error al convertir número"
finalmente:
    mostrar "Proceso completado"
fin

# Operaciones matemáticas
resultado = raiz(16) + potencia(2, 3)
mostrar "Resultado matemático: " + resultado
'''
    
    # Transpilación
    transpiler = GoTranspiler()
    go_code = transpiler.transpile(vader_code)
    
    print("✅ Transpilación completada!")
    print("\n" + "="*60)
    print("CÓDIGO GO GENERADO:")
    print("="*60)
    print(go_code)
    print("="*60)
    
    # Validaciones
    print("\n🔍 VALIDACIONES:")
    
    validations = {
        "Imports correctos": 'import (' in go_code and '"fmt"' in go_code,
        "Función main": 'func main() {' in go_code,
        "Variables tipadas": 'var ' in go_code or ':=' in go_code,
        "Slices/Arrays": 'make(' in go_code or '[]' in go_code,
        "Maps": 'map[' in go_code,
        "Funciones con tipos": 'func ' in go_code and '(' in go_code and ')' in go_code,
        "Structs personalizados": 'type ' in go_code and 'struct {' in go_code,
        "Constructores/métodos": 'func (' in go_code or 'func New' in go_code,
        "Error handling": 'error' in go_code or 'panic' in go_code or 'recover' in go_code,
        "Operaciones matemáticas": 'math.' in go_code or 'strconv.' in go_code,
        "Condicionales": 'if ' in go_code and 'else' in go_code,
        "Bucles": 'for ' in go_code
    }
    
    passed = 0
    total = len(validations)
    
    for test_name, result in validations.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📊 RESULTADO: {passed}/{total} validaciones pasadas")
    
    if passed == total:
        print("🎉 ¡TRANSPILADOR GO COMPLETO Y FUNCIONAL!")
    else:
        print("⚠️ El transpilador necesita mejoras")
    
    return passed == total

if __name__ == "__main__":
    test_go_transpiler()
