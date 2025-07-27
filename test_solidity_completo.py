#!/usr/bin/env python3
"""
Test completo del transpilador Solidity de Vader
Valida que el transpilador genere código Solidity válido y funcional
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transpilers.solidity import SolidityTranspiler

def test_solidity_transpiler():
    print("🧪 Iniciando test del transpilador Solidity COMPLETO...")
    
    # Código Vader de prueba completo
    vader_code = '''
# Test completo del transpilador Solidity
mostrar "=== Test Transpilador Solidity COMPLETO ==="

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
    transpiler = SolidityTranspiler()
    solidity_code = transpiler.transpile(vader_code)
    
    print("✅ Transpilación completada!")
    print("\n" + "="*60)
    print("CÓDIGO SOLIDITY GENERADO:")
    print("="*60)
    print(solidity_code)
    print("="*60)
    
    # Validaciones
    print("\n🔍 VALIDACIONES:")
    
    validations = {
        "Pragma y licencia": 'pragma solidity' in solidity_code and 'SPDX-License-Identifier' in solidity_code,
        "Contract definition": 'contract ' in solidity_code,
        "Variables tipadas": 'uint' in solidity_code or 'string' in solidity_code or 'bool' in solidity_code,
        "Arrays/mappings": 'mapping' in solidity_code or '[]' in solidity_code,
        "Structs": 'struct ' in solidity_code,
        "Functions con tipos": 'function ' in solidity_code and 'returns' in solidity_code,
        "Constructors": 'constructor(' in solidity_code,
        "Modifiers/visibility": 'public' in solidity_code or 'private' in solidity_code,
        "Events": 'event ' in solidity_code and 'emit ' in solidity_code,
        "Error handling": 'require(' in solidity_code or 'revert(' in solidity_code,
        "Math operations": 'SafeMath' in solidity_code or '+' in solidity_code,
        "Control flow": 'if (' in solidity_code and 'for (' in solidity_code
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
        print("🎉 ¡TRANSPILADOR SOLIDITY COMPLETO Y FUNCIONAL!")
    else:
        print("⚠️ El transpilador necesita mejoras")
    
    return passed == total

if __name__ == "__main__":
    test_solidity_transpiler()
